from datetime import datetime
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
    strava_last_queried = db.Column(db.Integer)
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

    def strava_import(self):
        if self.strava_code is None:
            return False
        token = self.get_strava_token()
        if self.strava_last_queried is None:
            self.strava_last_queried = 0
        response = requests.get(
            'https://www.strava.com/api/v3/athlete/activities',
            headers={
                    'Authorization': f'Bearer {token}'
            },
            params={
                'per_page': 200,
                'after': self.strava_last_queried
            }
        )
        self.strava_last_queried = int(time.time())
        response_json = json.loads(response.text)
        for activity in response_json:
            if activity['type'] == 'Run' or activity['type'] == 'Walk':
                distance = float(activity['distance']) / 1609.34
                duration = float(activity['elapsed_time']) / 60
                points = int(distance * 10)
                self.add_points(points)
                workout = Workout(
                    user_id=self.id,
                    distance=distance,
                    duration=duration,
                    type='Running (Strava imported)',
                    time=datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ').timestamp(),
                    points=points
                )
            elif activity['type'] == 'Ride':
                distance = float(activity['distance']) / 1609.34
                duration = float(activity['elapsed_time']) / 60
                points = int(distance * 50.31)
                self.add_points(points)
                workout = Workout(
                    user_id=self.id,
                    distance=distance,
                    duration=duration,
                    type='Biking (Strava imported)',
                    time=datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ').timestamp(),
                    points=points
                )
            elif activity['type'] == 'Swim':
                distance = float(activity['distance']) / 1609.34
                duration = float(activity['elapsed_time']) / 60
                points = int(duration * 7.2)
                self.add_points(points)
                workout = Workout(
                    user_id=self.id,
                    type='Swimming (Strava imported)',
                    distance=distance,
                    duration=duration,
                    time=datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ').timestamp(),
                    points=points
                )
            else:
                continue
            db.session.add(workout)
            db.session.commit()
        return True


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.Integer)
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
        elif self.type == "Running (Strava imported)":
            return f'Ran {self.distance:0.2f} miles in {self.duration:0.2f} minutes'
        elif self.type == "Biking (Strava imported)":
            return f'Biked {self.distance:0.2f} miles in {self.duration:0.2f} minutes'
        elif self.type == "Swimming (Strava imported)":
            return f'Swam {self.distance:0.2f} miles in {self.duration:0.2f} minutes'
        else:
            return 'Error'
