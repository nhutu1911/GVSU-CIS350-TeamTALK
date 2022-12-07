import time
from datetime import datetime

from flask import render_template
from flask import flash
from flask import Blueprint
from flask_login import current_user, login_required
from flask import request
from . import db

from .models import User, Workout

main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template('index.html')


@main.route('/user/', methods=["POST", "GET"])
@login_required
def user():
    if request.method == "POST":  # Submitting a manual workout
        try:
            if request.form.get("form") == "workout":
                if request.form['dropdownmenu'] == 'Running':
                    duration = float(request.form['duration'])
                    distance = float(request.form['distance'])
                    points = int(distance * 10)
                    User.add_points(current_user, points)
                    workout = Workout(type=request.form['dropdownmenu'], user_id=current_user.id, time=int(time.time()), points=points, duration=duration, distance=distance)
                    db.session.add(workout)
                    db.session.commit()
                elif request.form['dropdownmenu'] == 'Biking':
                    duration = float(request.form['duration'])
                    distance = float(request.form['distance'])
                    points = int(distance * 50.31)
                    User.add_points(current_user, points)
                    workout = Workout(type=request.form['dropdownmenu'], user_id=current_user.id, time=int(time.time()), points=points, duration=duration, distance=distance)
                    db.session.add(workout)
                    db.session.commit()
                elif request.form['dropdownmenu'] == 'Swimming':
                    duration = float(request.form['duration'])
                    distance = float(request.form['distance'])
                    points = int(duration * 7.2)
                    User.add_points(current_user, points)
                    workout = Workout(type=request.form['dropdownmenu'], user_id=current_user.id, time=int(time.time()), points=points, duration=duration, distance=distance)
                    db.session.add(workout)
                    db.session.commit()
                elif request.form['dropdownmenu'] == 'Weights':
                    weight = float(request.form['weight'])
                    reps = int(request.form['reps'])
                    sets = int(request.form['sets'])
                    points = int(reps * 1 * sets * weight)
                    User.add_points(current_user, points)
                    workout = Workout(type=request.form['dropdownmenu'], user_id=current_user.id, time=int(time.time()), points=points, weight=weight, reps=reps, sets=sets)
                    db.session.add(workout)
                    db.session.commit()
                elif request.form['dropdownmenu'] == 'Yoga':
                    duration = float(request.form['duration'])
                    points = int(duration * 3.42)
                    User.add_points(current_user, points)
                    workout = Workout(type=request.form['dropdownmenu'], user_id=current_user.id, time=int(time.time()), points=points, duration=duration)
                    db.session.add(workout)
                    db.session.commit()
                elif request.form['dropdownmenu'] == 'Other':
                    points = int(request.form['calories'])
                    User.add_points(current_user, points)
                    workout = Workout(type=request.form['dropdownmenu'], user_id=current_user.id, time=int(time.time()), points=points)
                    db.session.add(workout)
                    db.session.commit()
                flash("Activity added! Good job!", "success")
        except Exception:
            flash("Form data error, try again", "danger")
        if request.form.get("form") == "strava":
            if User.strava_import(current_user):
                flash('Successfully imported your Strava history!', "success")
            else:
                flash('Strava import failed, try again', "danger")
    # Strava Authentication
    if request.args:
        args = request.args
        if args.get('code') and args.get('scope') == 'read,activity:read_all':
            User.set_strava_code(current_user, args.get('code'))
            db.session.commit()
            flash("Strava account linked!", "success")
        elif args.get('error'):
            flash("Authentication failed. Did you click Authorize with the correct permissions?", "danger")
    return render_template('user.html', user=current_user)


@main.route('/user/<username>')
@login_required
def user_profile(username):
    temp = User.query.filter_by(username=username).first()
    workout_history = temp.workout_history.order_by(Workout.time.desc()).all()
    return render_template('user_profile.html', user=temp, workout_history=workout_history, Workout=Workout, datetime=datetime)


@main.route('/challenges/', methods=["POST", "GET"])
@login_required
def challenges():
    if request.method == "POST":
        if request.form['challenge'] == 'Complete Challenge 3':
            points3 = current_user.points + 300
            User.set_points(current_user, points3)
            db.session.commit()
            return render_template('user.html', user=current_user)
        elif request.form['challenge'] == 'Complete Challenge 2':
            points2 = current_user.points + 200
            User.set_points(current_user, points2)
            db.session.commit()
            return render_template('user.html', user=current_user)
        elif request.form['challenge'] == 'Complete Challenge 1':
            points = current_user.points+100
            User.set_points(current_user, points)
            db.session.commit()
            return render_template('user.html', user=current_user)
    return render_template('challenges.html')


@main.route('/leaderboard/')
def leaderboard():
    users = User.query.order_by(User.points.desc()).all()
    return render_template('leaderboard.html', users=users)
