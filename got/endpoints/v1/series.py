# -*- coding: utf-8 -*-
"""
Series endpoints

.. moduleauthor:: Amir Mofakhar <amir@mofakhar.info>

Python Version: 3.7

"""
from typing import Dict, Any, List
import logging

from flask import Blueprint

from got.models.got import GOT


bp = Blueprint("game_of_thrones", __name__)

_LOG = logging.getLogger(__name__)


@bp.route("/", methods=["GET"], defaults={"id": None})
@bp.route("/<id>", methods=["GET"])
def game_of_thrones(id: int) -> Dict[Any, Any]:
    """
    endpoint to return all episodes
    """
    if id:
        episodes = GOT.query.filter_by(id=id).all()
    else:
        episodes = GOT.query.all()

    response = _get_response(episodes)
    _LOG.debug("returning episodes")

    return response


@bp.route("/high_rate/", methods=["GET"], defaults={"season": None})
@bp.route("/high_rate/<season>", methods=["GET"])
def game_of_thrones_high_imdb(season: int) -> Dict[Any, Any]:
    """
    endpoint to return episodes with imdb rating greater than 8.8
    """
    if season:
        episodes = GOT.query.filter(GOT.imdb_rating > 8.8, GOT.season == season).all()
    else:
        episodes = GOT.query.filter(GOT.imdb_rating > 8.8).all()

    response = _get_response(episodes)

    _LOG.debug("returning high imdb rates")
    return response


def _get_response(episodes: GOT) -> dict:
    response = {"game_of_thrones": []}  # type: Dict[str, List[Any]]
    for episode in episodes:
        response["game_of_thrones"].append(episode.to_dict())

    return response
