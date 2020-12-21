# -*- coding: utf-8 -*-
"""
Flask application

.. moduleauthor:: Amir Mofakhar <amir@mofakhar.info>

Python Version: 3.7

"""
import logging
import sys
import time

from flask import Flask
from sqlalchemy.exc import InterfaceError  # type: ignore

from got.endpoints.v1 import series as series_v1, comments as comments_v1
from got.database import db
from got.utils.omdb import fetch_got_data
from got import settings


_LOG = logging.getLogger()

LOG_FORMATTER = logging.Formatter(
    "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S +0000"
)


def _init_logger() -> None:  # pragma: no cover

    log_level = settings.LOG_LEVEL
    root = logging.getLogger()
    root.setLevel(log_level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    ch.setFormatter(LOG_FORMATTER)
    root.addHandler(ch)


def _init_mysql(api: Flask) -> None:  # pragma: no cover
    mysql_db = settings.DB_NAME
    mysql_user = settings.DB_USER
    mysql_pass = settings.DB_PASSWORD
    mysql_host = settings.DB_HOST

    connection_string = f"mysql+mysqlconnector://{mysql_user}:{mysql_pass}@{mysql_host}/{mysql_db}?charset=utf8"
    _LOG.info(f"Connecting to: {mysql_host}")
    api.config["SQLALCHEMY_DATABASE_URI"] = connection_string


def create_app(testing=False, *args, **kwargs) -> Flask:  # pragma: no cover

    api = Flask(__name__)

    api.register_blueprint(series_v1.bp, url_prefix="/v1")
    api.register_blueprint(comments_v1.bp, url_prefix="/v1")

    api.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    api.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

    if testing:
        api.config["TESTING"] = True
        api.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
    else:  # pragma: no cover
        _init_logger()
        _init_mysql(api)

    db.init_app(api)

    try:
        db.create_all(app=api)
    except InterfaceError:
        _LOG.error("Could not connect to database! trying again in 10 seconds!")
        time.sleep(10)
        exit(2)

    if not testing:  # pragma: no cover
        fetch_got_data(api)

    api.app_context().push()
    _LOG.info("Server is ready now!")
    return api
