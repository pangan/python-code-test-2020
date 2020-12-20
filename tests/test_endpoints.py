# -*- coding: utf-8 -*-
from flask import json

from tests.base import BaseTestCase

from got.models.comments import Comments


class SeriesTestCase(BaseTestCase):
    def test_get_all_episodes(self):
        self.insert_sample_got_data(title="t1", season=1, episode=1)
        self.insert_sample_got_data(title="t2", season=1, episode=2)
        self.insert_sample_got_data(title="t3", season=2, episode=1)
        response = self.app.get("/v1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

        expcted_responsre = {"game_of_thrones": []}
        season = 1
        episode = 0
        for id in range(1, 4):
            if id == 3:
                episode = 1
                season = 2
            else:
                episode += 1

            expcted_responsre["game_of_thrones"].append(
                {
                    "title": f"t{id}",
                    "released": "2021-01-01",
                    "id": id,
                    "imdb_id": "112211221",
                    "imdb_rating": 1.0,
                    "season": season,
                    "episode": episode,
                }
            )
        self.assertDictEqual(json.loads(response.data), expcted_responsre)

    def test_get_episode_by_id(self):
        self.insert_sample_got_data(title="t1", season=1, episode=1)
        self.insert_sample_got_data(title="t2", season=1, episode=2)
        response = self.app.get("/v1/1")
        expected_response = {
            "game_of_thrones": [
                {
                    "title": "t1",
                    "released": "2021-01-01",
                    "id": 1,
                    "imdb_id": "112211221",
                    "imdb_rating": 1.0,
                    "season": 1,
                    "episode": 1,
                }
            ]
        }

        self.assertDictEqual(json.loads(response.data), expected_response)

    def test_get_imdb_high_rate(self):
        self.insert_sample_got_data(title="t1", season=1, episode=1, imdb_rate=9.0)
        self.insert_sample_got_data(title="t2", season=1, episode=2, imdb_rate=8.8)
        self.insert_sample_got_data(title="t3", season=2, episode=1, imdb_rate=7.8)
        self.insert_sample_got_data(title="t4", season=2, episode=2, imdb_rate=8.9)

        response = self.app.get("/v1/high_rate/")

        expected_response = {
            "game_of_thrones": [
                {
                    "title": "t1",
                    "released": "2021-01-01",
                    "id": 1,
                    "imdb_id": "112211221",
                    "imdb_rating": 9.0,
                    "season": 1,
                    "episode": 1,
                },
                {
                    "title": "t4",
                    "released": "2021-01-01",
                    "id": 4,
                    "imdb_id": "112211221",
                    "imdb_rating": 8.9,
                    "season": 2,
                    "episode": 2,
                },
            ]
        }

        self.assertDictEqual(json.loads(response.data), expected_response)

    def test_get_imdb_high_rate_season(self):
        self.insert_sample_got_data(title="t1", season=1, episode=1, imdb_rate=9.0)
        self.insert_sample_got_data(title="t2", season=1, episode=2, imdb_rate=8.8)
        self.insert_sample_got_data(title="t3", season=2, episode=1, imdb_rate=7.8)
        self.insert_sample_got_data(title="t4", season=2, episode=2, imdb_rate=8.9)

        response = self.app.get("/v1/high_rate/2")

        expected_response = {
            "game_of_thrones": [
                {
                    "title": "t4",
                    "released": "2021-01-01",
                    "id": 4,
                    "imdb_id": "112211221",
                    "imdb_rating": 8.9,
                    "season": 2,
                    "episode": 2,
                },
            ]
        }

        self.assertDictEqual(json.loads(response.data), expected_response)


class CommentsTestCase(BaseTestCase):
    def test_read_comments_of_an_episode(self):
        self.insert_sample_comment(body="body1", author="auther1")
        self.insert_sample_comment(body="body2", author="auther2")
        self.insert_sample_comment(body="body3", episode_id=2)
        response = self.app.get("/v1/comment/1")

        actual_response = json.loads(response.data)

        actual_comments = actual_response["comments"]
        for id in range(1, 2):
            actual_author = actual_comments[id - 1]["author"]
            self.assertEqual(actual_author, f"auther{id}")

    def test_post_comment(self):
        self.insert_sample_got_data()
        sample_comment = {
            "body": "foo bar foo",
            "author": "Amir",
        }
        response = self.app.post("/v1/comment/1", json=sample_comment)

        comments_from_db = Comments.query.all()

        self.assertEqual(len(comments_from_db), 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(comments_from_db[0].body, sample_comment["body"])
        self.assertEqual(comments_from_db[0].author, sample_comment["author"])
        self.assertEqual(comments_from_db[0].episode_id, 1)

    def test_post_comment_with_invalid_payload_returns_400(self):
        self.insert_sample_got_data()
        invalid_payload = {"foo": "bar"}
        response = self.app.post("/v1/comment/1", json=invalid_payload)
        comments_from_db = Comments.query.all()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(comments_from_db), 0)

    def test_post_comment_with_invalid_episode_returns_400(self):
        self.insert_sample_got_data()
        sample_comment = {
            "body": "foo bar foo",
            "author": "Amir",
        }
        response = self.app.post("/v1/comment/2", json=sample_comment)
        comments_from_db = Comments.query.all()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(comments_from_db), 0)

    def test_delete_comment(self):
        self.insert_sample_comment()
        comments_before_delete = Comments.query.all()
        response = self.app.delete("/v1/comment/1")
        comments_after_delete = Comments.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(comments_before_delete), 1)
        self.assertEqual(len(comments_after_delete), 0)

    def test_delete_comment_with_invalid_id_returns_400(self):
        # database is empty so comment 1 does not exist!
        response = self.app.delete("/v1/comment/1")
        self.assertEqual(response.status_code, 400)

    def test_update_comment(self):
        self.insert_sample_comment(body="first body", author="person 1")

        payloads = [
            {"body": "second body"},
            {"author": "person 2"},
            {"episode_id": 2},
            {"body": "third body", "author": "person 3", "episode_id": 3},
        ]
        for update_payload in payloads:
            response = self.app.put("/v1/comment/1", json=update_payload)
            comment = Comments.query.filter(Comments.id == 1).first()
            comment_dict = comment.to_dict()

            self.assertEqual(response.status_code, 200)
            for key, value in update_payload.items():
                self.assertEqual(comment_dict[key], value)

    def test_update_comment_with_invalid_payload_returns_400(self):
        self.insert_sample_comment()
        response = self.app.put("/v1/comment/1")
        self.assertEqual(response.status_code, 400)

    def test_update_comment_with_invalid_id_returns_400(self):
        self.insert_sample_comment()
        payload = {"body": "test"}
        not_exist_id = 2
        response = self.app.put(f"/v1/comment/{not_exist_id}", json=payload)
        self.assertEqual(response.status_code, 400)
