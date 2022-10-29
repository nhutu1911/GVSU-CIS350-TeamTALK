from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route('/user/')
def user():
    if current_user:
        return render_template('user.html', user=current_user)
    return redirect(url_for('auth.login'))

@main.route('/challenges/')
def challenges():
    return render_template('challenges.html')

@main.route('/leaderboard/')
def leaderboard():
    return render_template('leaderboard.html')

