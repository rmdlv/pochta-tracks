from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from db.session import get_db

from db.models import Tracks

import json


router = APIRouter()


@router.get("/get_data")
async def get_data(db: Session = Depends(get_db)):
    query = db.query(Tracks.coords.ST_AsGeoJSON()).all()

    return {
        "type": "FeatureCollection",
        "features": [json.loads(row[0]) for row in query],
    }
