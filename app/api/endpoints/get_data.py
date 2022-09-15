from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from db.session import get_db
from sqlalchemy.future import select

from db.models import Tracks

import json
from geojson import Feature, FeatureCollection


router = APIRouter()


def get_geojson():
    tracks = select(Tracks)
    return select(tracks.c.from_post, tracks.c.to_post, tracks.c.coords.ST_AsGeoJSON())


@router.get("/get_data")
async def get_data(db: Session = Depends(get_db)):
    query = db.execute(get_geojson())

    features = []
    for row in query:
        geometry = json.loads(row[2])
        properties = {"from_post": row[0], "to_post": row[1]}
        features.append(Feature(geometry=geometry, properties=properties))

    return FeatureCollection(features)
