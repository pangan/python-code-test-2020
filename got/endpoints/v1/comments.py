# -*- coding: utf-8 -*-
"""
Comments endpoints

.. moduleauthor:: Amir Mofakhar <amir@mofakhar.info>

Python Version: 3.7

"""
import logging
from typing import Dict, Any, List

from flask import Blueprint, request

from got.models.comments import Comments
from got.models.got import GOT

from got.database import db


bp = Blueprint("comments", __name__)

_LOG = logging.getLogger(__name__)


@bp.route("/comment/<episode_id>", methods=["GET"])
def get_comment(episode_id: int) -> Dict[Any, Any]:
    """
    endpoint to get comments of an episode
    """
    _LOG.debug(f"returning comments for episode {episode_id}")
    response = {"comments": []}  # type: Dict[str, List[Any]]
    comments_list = Comments.query.filter(Comments.episode_id == episode_id).all()
    for comment in comments_list:
        response["comments"].append(comment.to_dict())

    return response


@bp.route("/comment/<episode_id>", methods=["POST"])
def post_comment(episode_id):
    """
    endpoint to write comments for an episode
    """

    episode = GOT.query.filter(GOT.id == episode_id).all()
    if len(episode) == 0:
        return "Invalid episode ID!", 400
    comment = Comments()

    try:
        content = request.get_json()
        comment.body = content["body"]
        comment.author = content["author"]
    except Exception:
        return "Invalid payload", 400

    comment.episode_id = episode_id

    db.session.add(comment)
    db.session.commit()

    _LOG.debug(f"creating comments for episode {episode_id}")
    return "OK"


@bp.route("/comment/<comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    """
    endpoint to delete a comments
    """

    comment = Comments.query.filter(Comments.id == comment_id).first()
    if not comment:
        return "Invalid comment ID!", 400

    db.session.delete(comment)
    db.session.commit()

    return "OK"


@bp.route("/comment/<comment_id>", methods=["PUT"])
def put_comment(comment_id):
    """
    endpoint to update a comments
    """

    comment = Comments.query.filter(Comments.id == comment_id).first()
    if not comment:
        return "Invalid comment ID!", 400

    try:
        content = request.get_json()
        body = content.get("body")
        author = content.get("author")
        episode_id = content.get("episode_id")
    except Exception:
        return "Invalid payload", 400

    if body:
        comment.body = body
    if author:
        comment.author = author
    if episode_id:
        comment.episode_id = episode_id

    db.session.commit()

    return "OK"
