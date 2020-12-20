# -*- coding: utf-8 -*-
from tests.base import BaseTestCase
import json

from httpretty import HTTPretty

from got.utils.omdb import fetch_got_data
from got import settings

from got.models.got import GOT


class OMDbTestCase(BaseTestCase):
    def setUp(self):
        super(OMDbTestCase, self).setUp()
        HTTPretty.enable()
        settings.OMDB_URL = "http://www.omdbapi.com"
        settings.OMDB_KEY = "fake_key"
        self.series_title = "Game of Thrones"

    def tearDown(self):
        super(OMDbTestCase, self).tearDown()
        HTTPretty.disable()

    def test_fetch_got_data(self):
        omdb_bodies = [
            {
                "Title": "Game of Thrones",
                "Season": "1",
                "totalSeasons": "2",
                "Episodes": [
                    {
                        "Title": "title_1",
                        "Released": "2011-04-17",
                        "Episode": "1",
                        "imdbRating": "8.5",
                        "imdbID": "112233445",
                    },
                    {
                        "Title": "title_2",
                        "Released": "2011-04-17",
                        "Episode": "2",
                        "imdbRating": "8.4",
                        "imdbID": "112233446",
                    },
                ],
                "Response": "True",
            },
            {
                "Title": "Game of Thrones",
                "Season": "2",
                "totalSeasons": "2",
                "Episodes": [
                    {
                        "Title": "title_3",
                        "Released": "2011-04-17",
                        "Episode": "1",
                        "imdbRating": "7.5",
                        "imdbID": "112233447",
                    }
                ],
                "Response": "True",
            },
        ]

        expected_records = []
        record_id = 0
        season = 0
        for omdb_response in omdb_bodies:
            season += 1
            HTTPretty.register_uri(
                HTTPretty.GET,
                f"http://www.omdbapi.com/?t={self.series_title}&Season={season}&apikey={settings.OMDB_KEY}",
                match_querystring=True,
                body=json.dumps(omdb_response),
            )
            for episode in omdb_response["Episodes"]:

                record_id += 1

                expected_records.append(
                    {
                        "id": record_id,
                        "season": int(omdb_response["Season"]),
                        "episode": int(episode["Episode"]),
                        "title": episode["Title"],
                        "released": episode["Released"],
                        "imdb_rating": float(episode["imdbRating"]),
                        "imdb_id": episode["imdbID"],
                    },
                )

        fetch_got_data(self.api)

        total_records = GOT.query.all()

        self.assertEqual(3, len(total_records))

        actual_records = []
        for record in total_records:
            actual_records.append(record.to_dict())

        self.assertListEqual(actual_records, expected_records)

    def test_running_fetch_got_data_multiple_times_updates_records_not_insert(self):

        self.insert_sample_got_data()
        omdb_response = {
            "Title": "Game of Thrones",
            "Season": "1",
            "totalSeasons": "1",
            "Episodes": [
                {
                    "Title": "title_1",
                    "Released": "2011-04-17",
                    "Episode": "1",
                    "imdbRating": "8.5",
                    "imdbID": "112233445",
                },
                {
                    "Title": "title_2",
                    "Released": "2011-04-17",
                    "Episode": "2",
                    "imdbRating": "8.4",
                    "imdbID": "112233446",
                },
            ],
            "Response": "True",
        }
        season = 1
        HTTPretty.register_uri(
            HTTPretty.GET,
            f"http://www.omdbapi.com/?t={self.series_title}&Season={season}&apikey={settings.OMDB_KEY}",
            match_querystring=True,
            body=json.dumps(omdb_response),
        )

        fetch_got_data(self.api)

        total_records = GOT.query.all()

        self.assertEqual(2, len(total_records))
        expected_records = []
        record_id = 0

        for episode in omdb_response["Episodes"]:
            record_id += 1
            expected_records.append(
                {
                    "id": record_id,
                    "season": int(omdb_response["Season"]),
                    "episode": int(episode["Episode"]),
                    "title": episode["Title"],
                    "released": episode["Released"],
                    "imdb_rating": float(episode["imdbRating"]),
                    "imdb_id": episode["imdbID"],
                },
            )

        actual_records = []
        for record in total_records:
            actual_records.append(record.to_dict())

        self.assertListEqual(expected_records, actual_records)
