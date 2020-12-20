# -*- coding: utf-8 -*-
"""
Comments Game of Thrones seasons model

.. moduleauthor:: Amir Mofakhar <amir@mofakhar.info>

Python Version: 3.7
"""
from typing import Dict

from sqlalchemy import Column  # type: ignore
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DATE, FLOAT  # type: ignore

from got.database import db


class GOT(db.Model):
    __tablename__ = "got"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    season = Column(INTEGER, nullable=False)
    episode = Column(INTEGER, nullable=False)
    title = Column(VARCHAR(255), nullable=False)
    released = Column(DATE, nullable=False)
    imdb_rating = Column(FLOAT(4, 2), nullable=False)
    imdb_id = Column(VARCHAR(9), nullable=False)

    def to_dict(self) -> Dict:
        return {
            "season": self.season,
            "episode": self.episode,
            "title": self.title,
            "released": str(self.released),
            "imdb_rating": self.imdb_rating,
            "imdb_id": self.imdb_id,
            "id": self.id,
        }
