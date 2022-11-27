from flask import render_template
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask_login import current_user
from flask import request
from . import db

from .models import User
from flask import Flask
main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route('/user/')
def user():
    if current_user:
        return render_template('user.html', user=current_user)
    return redirect(url_for('auth.login'))

@main.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user_profile.html', user=user)

@main.route('/challenges/', methods=["POST","GET"])
def challenges():
    if request.method == "POST":
        if request.form['challenge'] == 'Complete Challenge 3':
            points3= current_user.points +300
            User.set_points(current_user,points3)
            db.session.commit()
            return render_template('user.html', user=current_user)
        elif request.form['challenge'] == 'Complete Challenge 2':
            points2= current_user.points +200
            User.set_points(current_user,points2)
            db.session.commit()
            return render_template('user.html', user=current_user)
        elif request.form['challenge'] == 'Complete Challenge 1':
            points=current_user.points+100
            User.set_points(current_user,points)
            db.session.commit()
            return render_template('user.html', user=current_user)
    return render_template('challenges.html')

@main.route('/leaderboard/')
def leaderboard():
    users = User.query.order_by(User.points.desc()).all()
    return render_template('leaderboard.html', users=users)
