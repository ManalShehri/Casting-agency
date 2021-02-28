import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  @app.route('/test')
  def index():
    return 'test'


  # GET all actors 
  @app.route('/actors', methods=['GET'])
  def all_actors():
    return 'test'

  # GET all movies
  @app.route('/movies', methods=['GET'])
  def all_movies():
    return 'test'

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
    return 'test'

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