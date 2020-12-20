# -*- coding: utf-8 -*-
"""
Settings

.. moduleauthor:: Amir Mofakhar <amir@mofakhar.info>

Python Version: 3.7

"""
from os import environ

# OMDB settings
OMDB_KEY = environ.get("OMDB_KEY")
OMDB_URL = environ.get("OMDB_URL")

# Database settings
DB_NAME = environ.get("DB_NAME", "DB_TEST_NAME")
DB_USER = environ.get("DB_USER", "DB_TEST_USER")
DB_PASSWORD = environ.get("DB_PASSWORD", "DB_TEST_PASSWORD")
DB_HOST = environ.get("DB_HOST", "DB_TEST_HOST")

# Log settings
LOG_LEVEL = environ.get("LOG_LEVEL", "DEBUG")
