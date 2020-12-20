# -*- coding: utf-8 -*-
from unittest import TestCase
from datetime import date


from got.app import create_app
from got.database import db
from got.models.got import GOT
from got.models.comments import Comments


class BaseTestCase(TestCase):
    def setUp(self):
        self.api = create_app(testing=True)
        self.app = self.api.test_client(self.api)
        self.maxDiff = None
        # db.app = self.api
        # db.create_all(app=self.api)
        # db.app = api

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def insert_sample_got_data(self, title="test", season=1, episode=1, imdb_rate=1.0):
        init_record = GOT(
            season=season,
            episode=episode,
            title=title,
            released=date(2021, 1, 1),
            imdb_id="112211221",
            imdb_rating=imdb_rate,
        )

        db.session.add(init_record)
        db.session.commit()

    def insert_sample_comment(self, body="foo", author="bar", episode_id=1):
        init_record = Comments(body=body, author=author, episode_id=episode_id)

        db.session.add(init_record)
        db.session.commit()
