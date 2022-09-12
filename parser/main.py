import requests
from bs4 import BeautifulSoup

from constants import DEFAULT_PARSER, USER_AGENT

from typing import List


def get_code_list() -> List[int]:
    response = requests.get(
        "https://indexphone.ru/post/1414662", headers={"User-Agent": USER_AGENT}
    )
    parser = BeautifulSoup(response.text, DEFAULT_PARSER)

    code_list = []
    for code_block in parser.find_all("td", class_="post-object-list-postalcode"):
        code_list.append(int(code_block.text))

    return code_list


def gen_track(post_code: int, month: int, id: int) -> int:
    # https://ru.wikipedia.org/wiki/Почтовый_идентификатор
    track_string = str(post_code) + str(month).zfill(2) + str(id).zfill(5)

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


if __name__ == "__main__":
    for code in get_code_list():
        for id in range(10):
            print(gen_track(code, 55, id))
