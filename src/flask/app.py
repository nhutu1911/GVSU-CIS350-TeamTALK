import os
from dotenv import load_dotenv

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)

app.secret_key = SECRET_KEY

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/user/')
def user():
    if 'username' in session:
        return render_template('user.html', name=session['username'])
    return render_template('login.html')

@app.route('/challenges/')
def challenges():
    return render_template('challenges.html')

@app.route('/leaderboard/')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('user'))
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('user'))
    return render_template('login.html')
