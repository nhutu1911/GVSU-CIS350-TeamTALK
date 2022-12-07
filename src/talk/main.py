from flask import render_template
from flask import flash
from flask import Blueprint
from flask_login import current_user, login_required
from flask import request
from . import db

from .models import User
main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template('index.html')


@main.route('/user/', methods=["POST", "GET"])
@login_required
def user():
    if request.method == "POST":
        if request.form:
            if request.form['dropdownmenu'] == 'Running':
                duration = float(request.form['duration'])
                distance = float(request.form['distance'])
                points = distance * 10 + current_user.points
                User.set_points(current_user, points)
                db.session.commit()
            elif request.form['dropdownmenu'] == 'Biking':
                duration = float(request.form['duration'])
                distance = float(request.form['distance'])
                points = distance * 50.31 + current_user.points
                User.set_points(current_user, points)
                db.session.commit()
            elif request.form['dropdownmenu'] == 'Swimming':
                duration = float(request.form['duration'])
                distance = float(request.form['distance'])
                points = duration * 7.2 + current_user.points
                User.set_points(current_user, points)
                db.session.commit()
            elif request.form['dropdownmenu'] == 'Weights':
                weight = float(request.form['weight'])
                reps = float(request.form['reps'])
                sets = float(request.form['sets'])
                points = reps * 1 * sets + current_user.points
                User.set_points(current_user, points)
                db.session.commit()
            elif request.form['dropdownmenu'] == 'Yoga':
                duration = float(request.form['duration'])
                points = duration * 3.42 + current_user.points
                User.set_points(current_user, points)
                db.session.commit()
            flash("Activity added! Good job!", "success")
    return render_template('user.html', user=current_user)


@main.route('/user/<username>')
@login_required
def user_profile(username):
    temp = User.query.filter_by(username=username).first()
    return render_template('user_profile.html', user=temp)


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
