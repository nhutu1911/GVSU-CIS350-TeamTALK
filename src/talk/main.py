from flask import render_template
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask_login import current_user

from .models import User


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
    users = User.query.order_by(User.points.desc()).all()
    return render_template('leaderboard.html', users=users)

