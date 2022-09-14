from sqlalchemy import Column, Integer
from geoalchemy2 import Geometry

from db.session import Base


class Tracks(Base):
    __tablename__ = "tracks"
    from_post = Column(Integer)
    to_post = Column(Integer)
    coords = Column(Geometry("LINESTRING"))
    id = Column(Integer, primary_key=True)
