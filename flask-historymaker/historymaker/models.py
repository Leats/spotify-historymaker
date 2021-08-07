from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Album(db.Model):
    title = db.Column(db.String, nullable=False)
    uri = db.Column(db.String, nullable=False)
    artisturi = db.Column(db.String, db.ForeignKey("artist.uri"))
    id = db.Column(db.String, nullable=False, primary_key=True)

    def __repr__(self):
        return f"<Album {self.uri}>"


class Artist(db.Model):
    name = db.Column(db.String, nullable=False)
    uri = db.Column(db.String, nullable=False)
    id = db.Column(db.String, nullable=False, primary_key=True)
    genre = db.Column(db.ARRAY(db.String), nullable=False)

    def __repr__(self):
        return f"<Artist {self.uri}>"


class Context(db.Model):
    uri = db.Column(db.String, nullable=False, primary_key=True)
    type = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Context {self.uri}>"


class Played(db.Model):
    trackuri = db.Column(db.String, db.ForeignKey("track.uri"), nullable=False)
    artisturi = db.Column(db.String, db.ForeignKey("artist.uri"))
    contexturi = db.Column(db.String, db.ForeignKey("context.uri"))
    time = db.Column(db.DateTime, nullable=False, primary_key=True)

    def __repr__(self):
        return f"<Played {self.time}>"


class Track(db.Model):
    title = db.Column(db.String, nullable=False)
    uri = db.Column(db.String, nullable=False)
    artisturi = db.Column(db.String, db.ForeignKey("artist.uri"))
    albumuri = db.Column(db.String, db.ForeignKey("album.uri"))
    id = db.Column(db.String, nullable=False, primary_key=True)
    duration = db.Column(db.Integer)
    explicit = db.Column(db.Boolean)
    popularity = db.Column(db.Integer)
    tracknumber = db.Column(db.Integer)

    def __repr__(self):
        return f"<Track {self.id}>"
