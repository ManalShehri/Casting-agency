import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import * 

CASTING_ASSISTANT_TOKEN = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpSSXlGWVRJWGZMS21vQkZ2XzZIdCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ueGdqdTB3Yi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzZjNmNWNmNWU4M2MwMDZhNTA0OTg2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNDg0MjI1NCwiZXhwIjoxNjE0ODQ5NDU0LCJhenAiOiJlNHNJQUkxR2pTRnE1T3dsdzEwc2ZXUGgxWFlYN2pCciIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.Joeb8RLLBWkNtAtaYzKuYxq48Y9oSxVZuTWoxBSmWoaM2SkmamkEOjSehIUBxMjfZvl3uFMjue0kaHAV5wlhrxM_4HwqPyjVtMvqfX5tCs4iH3VsWxf9Zktz2tczq_jvgN_ok4YhO1NTF6f6injL3RWh-Ubu96A3oejaHzDU1KKknVfncoYBC75mCnVQuNIi0bwvdkNjO_5BrvWl2zl0pJWDmqc4yZuPZ2-xV_i7rCMJI84gdX8A97aIcMbzvmt_99aTu7Jp_sS5TA60na4Dg9SGJm9vDuwtDAOx7E8qOkzIdjNCIa9thXC19RGTbyMBJWC1MAoA6bSwbzphx_LL5Q')
CASTING_DIRECTOR_TOKEN = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpSSXlGWVRJWGZMS21vQkZ2XzZIdCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ueGdqdTB3Yi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzZjNmOTlmNWU4M2MwMDZhNTA0OWE3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNDg0MzE4NywiZXhwIjoxNjE0ODUwMzg3LCJhenAiOiJlNHNJQUkxR2pTRnE1T3dsdzEwc2ZXUGgxWFlYN2pCciIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.OcIr9emMYEDkc5FGz_gQPCz-FIbE17q3ePU__yVzoCPVXkXcQ9HhSTnj5C83ptqxnYIBuDEkA1yzJQl9tI8GNXMVh5TDXKNunYkjLz-5PkCGXSkrQBveKUVyfbT8EQk0L6Xg4Wm7rWaHJ3JzzghogNP5hvwlQrC29jpmMjIWb615Z_CkwpY91FPrqUVzMTplGRQ63cKFJ6NmwHjYQtcfP6G08ffAX8gDJxWXNsrsr7ZRpLPq0FRUOPl6V72eIVNmGbzc4keq1ZlPRzYBX8VoDZ7Pa51oZi1DpjquwlhJ0m2zOV2ZwfOqOy-O9r13_PDUnbEB6F9tw7S7IzBQf3t_KQ')
EXECUTIVE_PRODUCER_TOKEN = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpSSXlGWVRJWGZMS21vQkZ2XzZIdCJ9.eyJpc3MiOiJodHRwczovL2Rldi1ueGdqdTB3Yi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzZjQwMTFkYTk0MWYwMDcwNWQ3OWRmIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNDgzODIzMywiZXhwIjoxNjE0ODQ1NDMzLCJhenAiOiJlNHNJQUkxR2pTRnE1T3dsdzEwc2ZXUGgxWFlYN2pCciIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.Of4bstV0StKn5La8ElqgZvWf0fhefGSmiWrD9zfbEgBQ6vh62t9EmzaRkmbESER7VDhnsYFXaR8Wa6fVsi6LRGftA8SqVet2KrF9W2tIMdM7h_4haRGbjo82KAVcuzLi-BAupZ9o8K5896dJSylJx9FJMJ_oIQ7NVfUmbDONcVn_EKL4mBTgw4oUcq-EEemyI4iOQENX8dwBGZImgYSz2VmQWm1wVeM_uw_-I4f6FwmlNKrHQVIMy_3vNrnGOYhvyjOO9Pn0z432IBP3JrNFXaJIdQoRBQIr8C9X7Xnyc5x3c9lWDGqaQiH0EBng9HO09mIdYL4-F6AIoWUi6Q2Xig')

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency"
        self.DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
        self.DB_USER = os.getenv('DB_USER', 'manal')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', '123456m')
        self.DB_NAME = os.getenv('DB_NAME', 'casting_agency')
        self.database_path = "postgres://{}:{}@{}/{}".format(
            self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass
    
    ##### Test Cases #####


    ##### 1.CASTING_ASSISTANT #####


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


    ##### 2.CASTING_DIRECTOR #####


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


    ##### 3.EXECUTIVE_PRODUCER #####


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
