import requests
from bs4 import BeautifulSoup
from datetime import datetime
import psycopg2
from loguru import logger

from constants import DEFAULT_PARSER, USER_AGENT, DB_CREDENTIALS

from typing import List, Tuple

TRACKS_PER_POST = 10
DATE_NUMBER = 55  # January 1, 2021

TRACKING_BASE_URL = (
    "https://www.pochta.ru/tracking?"
    + "p_p_id=trackingPortlet_WAR_portalportlet&"
    + "p_p_lifecycle=2&"
    + "p_p_state=normal&"
    + "p_p_mode=view&"
    + "p_p_resource_id=tracking.get-by-barcodes&"
    + "p_p_cacheability=cacheLevelPage&"
    + "p_p_col_id=column-1&"
    + "p_p_col_count=1&"
    + "barcodes="
)
GEOCODE_BASE_URL = "https://www.pochta.ru/suggestions/v2/postoffice.find-nearest-by-postalcode-vacancies"

connection = psycopg2.connect(**DB_CREDENTIALS)
cursor = connection.cursor()


def get_code_list() -> List[int]:
    response = requests.get(
        "https://indexphone.ru/post/1414662", headers={"User-Agent": USER_AGENT}
    )
    parser = BeautifulSoup(response.text, DEFAULT_PARSER)

    for code_block in parser.find_all("td", class_="post-object-list-postalcode"):
        yield int(code_block.text)


def gen_track(post_code: int, month: int, id: int) -> int:
    # https://ru.wikipedia.org/wiki/Почтовый_идентификатор
    track_string = f"{post_code}{month:02d}{id:05d}"

    even, odd = [], []
    for position, digit in enumerate(track_string):
        digit = int(digit)

        if (position + 1) % 2 == 0:
            even.append(digit)
        else:
            odd.append(digit)

    checksum = 10 - (sum(odd) * 3 + sum(even)) % 10
    if checksum == 10:
        checksum = 0

    track_string += str(checksum)

    return int(track_string)


def get_dest_code(track_code: int) -> int:
    response = requests.get(TRACKING_BASE_URL + str(track_code))

    return response.json()["response"][0]["trackingItem"]["indexTo"]


def get_coords_by_code(post_code: int) -> Tuple[float]:
    response = requests.post(
        GEOCODE_BASE_URL,
        json={
            "currentDateTime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            "filters": [],
            "limit": 1,
            "offset": 0,
            "postalCode": post_code,
            "radius": 100,
        },
        headers={"User-Agent": USER_AGENT},
    )
    return (response.json()[0]["latitude"], response.json()[0]["longitude"])


if __name__ == "__main__":
    for post_code in get_code_list():
        origin_lat, origin_lon = get_coords_by_code(post_code)
        for id in range(TRACKS_PER_POST):
            track_code = gen_track(post_code, DATE_NUMBER, id)
            dest_code = get_dest_code(track_code)
            if dest_code:
                dest_lat, dest_lon = get_coords_by_code(dest_code)

                geometry = (
                    f"LINESTRING({origin_lon} {origin_lat},{dest_lon} {dest_lat})"
                )
                logger.info(geometry)
                cursor.execute(
                    "INSERT INTO tracks VALUES (%s, %s, ST_GeomFromText(%s, 4326))",
                    (post_code, dest_code, geometry),
                )

                connection.commit()
