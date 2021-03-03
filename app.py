import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import datetime
from models import *
from auth import *

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  # app.config.from_object('config.DatabaseURI')
  # db = SQLAlchemy(app)
  # migrate = Migrate(app, db)
  CORS(app)

  @app.route('/test')
  def index():
    return 'test'


  # GET all actors 
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def all_actors(token):
    return jsonify({
            'success': True,
            'actors':list(map(lambda x: x.json(), Actor.query.all())),
        }), 200

  # GET all movies
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def all_movies(token):
    return jsonify({
        'success': True,
        'movies': list(map(lambda x: x.json(), Movie.query.all())),
    }), 200

  # DELETE an actor
  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(token,id):
    try:
      actor = Actor.query.filter(Actor.id == id).one_or_none()
   
      if actor:
          actor.delete_from_db()
          return jsonify({
          'success': True,
          'Message': 'Actor deleted successfully'
          })
          
      else:
        return jsonify({
              'success': False,
              'message': 'Actor Not Found'
            }), 404 
            
    except Exception as e:
      return jsonify({
          'success': False,
          'Message': str(e),
        }), 500

  # DELETE a movie
  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(token,id):
    try:
      movie = Movie.query.filter(Movie.id == id).one_or_none()
   
      if movie:
          movie.delete_from_db()
          return jsonify({
          'success': True,
          'Message': 'Movie deleted successfully'
          })
          
      else:
        return jsonify({
              'success': False,
              'message': 'Movie Not Found'
            }), 404 

    except Exception as e:
      return jsonify({
          'success': False,
          'Message': str(e),
        }), 500

  # POST an actor
  @app.route('/actors/new', methods=['POST'])
  @requires_auth('post:actor')
  def add_actor(token):
    try:
      data = request.get_json()

      if data['name'] is not None:
        
        name = data['name']
        new_actor = Actor(name=data['name'],age=data['age'],gender=data['gender'],bio=data['bio'],image_link=data['image_link']) 
        new_actor.save_to_db()
          
        return jsonify({
          'success': True,
          'new_actor': new_actor.json(),
        }), 200

      else:
        return jsonify({
          'success': False,
          'Message': 'Name should be provided',
        }), 500

    except Exception as e:
      return jsonify({
          'success': False,
          'Message': str(e),
        }), 500

  # POST a movie
  @app.route('/movies/new', methods=['POST'])
  @requires_auth('post:movie')
  def add_movie(token):
    try:
      data = request.get_json()

      if data['title'] is not None:
        
        title = data['title']
        new_movie = Movie(title=data['title'],release_date=data['release_date'],description=data['description'],director=data['director'],category=data['category'],image_link=data['image_link']) 
        new_movie.save_to_db()
          
        return jsonify({
          'success': True,
          'new_moive': new_movie.json(),
        }), 200

      else:
        return jsonify({
          'success': False,
          'Message': 'Title should be provided',
        }), 500

    except Exception as e:
      return jsonify({
          'success': False,
          'Message': str(e),
        }), 500


  # PATCH an actor
  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actor')
  def edit_actor(token,id):
    try:
      data = request.get_json() 
      actor = Actor.query.filter(Actor.id == id).one_or_none()
     
      if actor:
          if 'name' in data:
              actor.name = data['name']
          if 'age' in data:
              actor.age = data['age']
          if 'gender' in data:
              actor.gender = data['gender']
          if 'bio' in data:
              actor.bio = data['bio']
          if 'image_link' in data:
              actor.image_link = data['image_link']

          actor.save_to_db()
            
          return jsonify({
            'success': True,
            'message': 'Actor updated successfully',
            'actor': actor.json(),
          }), 200

      else:
          return jsonify({
            'success': False,
            'message': 'Actor Not Found'
          }), 404 

    except Exception as e:
      return jsonify({
          'success': False,
          'Message': str(e),
        }), 500

  # PATCH a movie
  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  def edit_movie(token,id):
    try:
      data = request.get_json() 
      movie = Movie.query.filter(Movie.id == id).one_or_none()
     
      if movie:
          if 'title' in data:
              movie.title = data['title']
          if 'release_date' in data:
              movie.release_date = data['release_date']
          if 'description' in data:
              movie.description = data['description']
          if 'director' in data:
              movie.director = data['director']
          if 'category' in data:
              movie.category = data['category']
          if 'image_link' in data:
              movie.image_link = data['image_link']

          movie.save_to_db()
            
          return jsonify({
            'success': True,
            'message': 'Movie updated successfully',
            'movie': movie.json(),
          }), 200

      else:
          return jsonify({
            'success': False,
            'message': 'Movie Not Found'
          }), 404 

    except Exception as e:
      return jsonify({
          'success': False,
          'Message': str(e),
        }), 500

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)