from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route('/user/')
def user():
    if 'username' in session:
        return render_template('user.html', name=session['username'])
    return render_template('login.html')

@main.route('/challenges/')
def challenges():
    return render_template('challenges.html')

@main.route('/leaderboard/')
def leaderboard():
    return render_template('leaderboard.html')

