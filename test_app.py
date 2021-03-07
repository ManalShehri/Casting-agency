import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *

CASTING_ASSISTANT_TOKEN = os.environ.get('CASTING_ASSISTANT_TOKEN')
CASTING_DIRECTOR_TOKEN = os.environ.get('CASTING_DIRECTOR_TOKEN')
EXECUTIVE_PRODUCER_TOKEN = os.environ.get('EXECUTIVE_PRODUCER_TOKEN')
DATABASE_URL = os.environ.get('DATABASE_URL')


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.environ.get('DB_HOST')
        self.DB_USER = os.environ.get('DB_USER')
        self.DB_PASSWORD = os.environ.get('DB_PASSWORD')
        self.DB_NAME = os.environ.get('DB_NAME')
        self.database_path_dev = "postgres://{}:{}@{}/{}".format(
            self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        self.database_path_prod = DATABASE_URL
        setup_db(self.app, self.database_path_prod)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    # Test Cases

    # 1.CASTING_ASSISTANT #

    # Test view all movies (success)

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    # Test view all movies (failure)
    def test_get_movies_not_allowed(self):
        res = self.client().delete(
            '/movies',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        self.assertEqual(res.status_code, 405)

    # Test view all actors (success)
    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    # Test view all actors (failure)
    def test_get_actors_not_allowed(self):
        res = self.client().delete(
            '/actors',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        self.assertEqual(res.status_code, 405)

    # 2.CASTING_DIRECTOR

    # Test add an actor (success)

    def test_add_actor(self):
        new_actor = {
            "name": "Angelina",
            "age": 45,
            "gender": "female",
            "image_link": "http:/image/Angelina_Jolie/1",
            "bio": "Angelina Jolie is an American actress, filmmaker, and humanitarian. The recipient of numerous accolades, including an Academy Award and three Golden Globe Awards."
        }
        res = self.client().post(
            '/actors/new',
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'},
            json=new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # Test add an actor (failure)
    def test_add_blank_actor(self):
        new_actor = {}
        res = self.client().post(
            '/movies/new',
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'},
            json=new_actor)
        # data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        # self.assertEqual(data["success"], False)

    # Test edit an actor (success)
    def test_edit_actor(self):
        update_actor = {
            'name': 'Angelina Jolie'
        }
        res = self.client().patch(
            '/actors/3',
            json=update_actor,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data["Message"], "Actor updated successfully")

    # Test edit an actor (failure)
    def test_edit_actor_not_authorized(self):
        update_actor = {
            'name': 'Angelina Jolie'
        }
        res = self.client().patch(
            '/actors/3',
            json=update_actor,
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        self.assertEqual(res.status_code, 401)

    # Test delete an actor (success)
    def test_delete_actor(self):
        res = self.client().delete(
            '/actors/1',
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["Message"], "Actor deleted successfully")

    # Test delete an actor (failure)
    def test_delete_actor_not_found(self):
        res = self.client().delete(
            '/actors/10000',
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["Message"], "Actor Not Found")

    # 3.EXECUTIVE_PRODUCER

    # Test add a movie (success)

    def test_add_movie(self):
        new_movie = {
            "title": "Frozen I",
            "release_date": "2013-11-19 00:00:00",
            "description": "Anna sets out on a journey with an iceman, Kristoff, and his reindeer, Sven, in order to find her sister, Elsa, who has the power to convert any object or person into ice.",
            "director": "Jennifer Lee,",
            "category": ["Drama"],
            "image_link": "http:/image/frozen/1"
        }
        res = self.client().post(
            '/movies/new',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'},
            json=new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # Test add a movie (failure)
    def test_add_blank_movie(self):
        new_movie = {}
        res = self.client().post(
            '/movies/new',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'},
            json=new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data["success"], False)

    # Test edit a movie (success)
    def test_edit_movie(self):
        update_movie = {
            'title': 'Frozen II',
            'release_date': "2019-11-19 00:00:00"
        }
        res = self.client().patch(
            '/movies/4',
            json=update_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data["Message"], "Movie updated successfully")

    # Test edit a movie (failure)
    def test_edit_movie_not_authorized(self):
        update_movie = {
            'title': 'Frozen II',
            'release_date': "2019-11-19 00:00:00"
        }
        res = self.client().patch(
            '/actors/3',
            json=update_movie,
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        self.assertEqual(res.status_code, 401)

    # # Test delete a movie (success)
    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/1',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["Message"], "Movie deleted successfully")

    # Test delete a movie (failure)
    def test_delete_movie_not_found(self):
        res = self.client().delete(
            '/movies/10000',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["Message"], "Movie Not Found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
