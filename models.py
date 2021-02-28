import json
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    release_date = db.Column(db.DateTime)
    description = db.Column(db.String(180))
    director = db.Column(db.String(80))
    category = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default = datetime.datetime.now)
    updated_at = db.Column(db.DateTime, onupdate = datetime.datetime.now)

class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(89))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    bio = db.Column(db.String(200))
    image_link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default = datetime.datetime.now)
    updated_at = db.Column(db.DateTime, onupdate = datetime.datetime.now)
