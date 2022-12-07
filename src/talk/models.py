import time

from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    points = db.Column(db.Integer)
    strava_code = db.Column(db.String(50))
    strava_token = db.Column(db.String(50))
    strava_refresh_token = db.Column(db.String(50))
    strava_expires_at = db.Column(db.Integer)
    strava_athlete = db.Column(db.String(2000))
    workout_history = db.relationship('Workout', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_points(self, points):
        self.points = points

    def add_points(self, points):
        self.points = self.points + points

    def set_strava_code(self, code):
        self.strava_code = code

    def set_strava_token(self, token, refresh_token, expires_at):
        self.strava_token = token
        self.strava_refresh_token = refresh_token
        self.strava_expires_at = expires_at

    def get_strava_token(self):
        if self.strava_token is None:
            response = requests.post(
                'https://www.strava.com/api/v3/oauth/token',
                data={
                    'client_id': '96464',
                    'client_secret': 'f521db270c56678723d4c467fe20a4430a343154',
                    'code': self.strava_code,
                    'grant_type': 'authorization_code'
                }
            )
            response_json = json.loads(response.text)
            self.set_strava_token(response_json['access_token'], response_json['refresh_token'], response_json['expires_at'])
            self.strava_athlete = str(response_json['athlete'])
            db.session.commit()
            return self.strava_token

        if self.strava_expires_at > int(time.time()):
            return self.strava_token
        else:
            response = requests.post(
                'https://www.strava.com/api/v3/oauth/token',
                data={
                    'client_id': '96464',
                    'client_secret': 'f521db270c56678723d4c467fe20a4430a343154',
                    'grant_type': 'refresh_token',
                    'refresh_token': self.strava_refresh_token
                }
            )
            response_json = json.loads(response.text)
            self.set_strava_token(response_json['access_token'], response_json['refresh_token'], response_json['expires_at'])
            db.session.commit()
            return self.strava_token


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.String(50))
    type = db.Column(db.String(50))
    duration = db.Column(db.Numeric)
    distance = db.Column(db.Numeric)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    points = db.Column(db.Integer)

    def __repr__(self):
        return '<Workout {}>'.format(self.id)

    def get_summary(self):
        if self.type == "Running":
            return f'Ran {self.distance:0.2f} miles in {self.duration:0.2f} minutes'
        elif self.type == "Biking":
            return f'Biked {self.distance:0.2f} miles in {self.duration:0.2f} minutes'
        elif self.type == "Swimming":
            return f'Swam {self.distance:0.2f} miles in {self.duration:0.2f} minutes'
        elif self.type == "Weights":
            return f'Lifted {self.weight:0.2f} pounds {self.reps} times for {self.sets} sets'
        elif self.type == "Yoga":
            return f'Practiced yoga for {self.duration:0.2f} minutes'
        elif self.type == "Other":
            return f'Manually entered burning {self.points} calories'
        else:
            return 'Error'
