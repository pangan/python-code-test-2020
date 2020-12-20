# -*- coding: utf-8 -*-
import requests
import logging
from datetime import datetime

from flask import Flask

from got import settings
from got.models.got import GOT
from got.database import db


_LOG = logging.getLogger(__name__)


def fetch_got_data(app: Flask) -> None:
    db.app = app
    series_title = "Game of Thrones"
    season = 1
    total_seasons = 2
    try:
        while total_seasons >= season:
            _LOG.info(f"Fetching data from OMDB: {series_title}, Season: {season}")
            url = f"{settings.OMDB_URL}/?t={series_title}&Season={season}&apikey={settings.OMDB_KEY}"
            response = requests.get(url).json()
            total_seasons = int(response["totalSeasons"])
            season += 1

            for episode in response["Episodes"]:
                series = GOT.query.filter_by(
                    season=response["Season"], episode=episode["Episode"]
                ).first()
                if not series:
                    series = GOT()

                series.title = episode["Title"]
                series.season = response["Season"]
                series.episode = episode["Episode"]
                series.imdb_id = episode["imdbID"]
                series.imdb_rating = episode["imdbRating"]
                series.released = datetime.strptime(episode["Released"], "%Y-%m-%d")
                db.session.add(series)

            db.session.commit()
    except Exception as e:  # pragma: no cover
        _LOG.error(str(e))
