# -*- coding: utf-8 -*-
"""
Comments model

.. moduleauthor:: Amir Mofakhar <amir@mofakhar.info>

Python Version: 3.7
"""
from datetime import datetime
from typing import Dict

from sqlalchemy import Column, ForeignKey  # type: ignore
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, TEXT, DATETIME  # type: ignore


from got.database import db


class Comments(db.Model):
    __tablename__ = "comments"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    episode_id = Column(INTEGER, ForeignKey("got.id"))
    body = Column(TEXT, nullable=True)
    author = Column(VARCHAR(255), nullable=False)
    time_stamp = Column(DATETIME, default=datetime.utcnow)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "body": self.body,
            "author": self.author,
            "time_stamp": self.time_stamp,
            "episode_id": self.episode_id,
        }
