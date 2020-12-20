# -*- coding: utf-8 -*-
"""
This module is for validating payloads

.. moduleauthor:: Amir Mofakhar <amir@mofakhar.info>

Python Version: 3.7
"""
from jsonschema import validate  # type: ignore


def validate_put_comment_payload(payload: dict) -> None:
    schema = {
        "type": "object",
        "properties": {
            "author": {"type": "string"},
            "body": {"type": "string"},
            "episode_id": {"type": "number"},
        },
        "anyOf": [
            {"required": ["author"]},
            {"required": ["body"]},
            {"required": ["episode_id"]},
        ],
    }

    validate(payload, schema)
