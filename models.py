import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')

database_path = "postgres://{}:{}@{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

# env is production
DATABASE_URL = os.environ.get('DATABASE_URL')
db = SQLAlchemy()


def setup_db(app, database_path=DATABASE_URL):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


movieCharacters = db.Table('movieCharacters', db.Model.metadata,
                           db.Column('movie_id', db.Integer,
                                     db.ForeignKey('Movie.id')),
                           db.Column('actor_id', db.Integer,
                                     db.ForeignKey('Actor.id'))
                           )


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    release_date = db.Column(db.DateTime)
    description = db.Column(db.String(180))
    director = db.Column(db.String(80))
    category = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now)
    actors = db.relationship(
        'Actor', secondary=movieCharacters, back_populates="movies")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'description': self.description,
            'director': self.director,
            'category': self.category,
            'image_link': self.image_link,
            'created_at': str(self.created_at.strftime("%Y-%m-%d %H:%M:%S")),
            'updated_at': str(self.updated_at),
        }


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(89))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    bio = db.Column(db.String(200))
    image_link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now)
    movies = db.relationship(
        "Movie", secondary=movieCharacters, back_populates="actors")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'bio': self.bio,
            'image_link': self.image_link,
            'created_at': str(self.created_at.strftime("%Y-%m-%d %H:%M:%S")),
            'updated_at': str(self.updated_at),
        }
