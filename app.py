import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import datetime
from models import *

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.config.from_object('config.DatabaseURI')
  db = SQLAlchemy(app)
  migrate = Migrate(app, db)
  CORS(app)

  @app.route('/test')
  def index():
    return 'test'


  # GET all actors 
  @app.route('/actors', methods=['GET'])
  def all_actors():
    return jsonify({
            'success': True,
            'actors':list(map(lambda x: x.json(), Actor.query.all())),
        }), 200

  # GET all movies
  @app.route('/movies', methods=['GET'])
  def all_movies():
    return jsonify({
        'success': True,
        'movies': list(map(lambda x: x.json(), Movie.query.all())),
    }), 200

  # DELETE an actor
  @app.route('/actors/<int:id>', methods=['DELETE'])
  def delete_actor():
    return 'test'

  # DELETE a movie
  @app.route('/movies/<int:id>', methods=['DELETE'])
  def delete_movie():
    return 'test'

  # POST an actor
  @app.route('/actors/new', methods=['POST'])
  def add_actor():
    return 'test'

  # POST a movie
  @app.route('/movies/new', methods=['POST'])
  def add_movie():
    try:
      data = request.get_json()

      if data['title'] is None:
        
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
          'Message': str(e) + 'is missing!',
        }), 500


  # PATCH an actor
  @app.route('/actors/<int:id>', methods=['PATCH'])
  def edit_actor():
    return 'test'

  # PATCH a movie
  @app.route('/movies/<int:id>', methods=['PATCH'])
  def edit_movie():
    return 'test'

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)