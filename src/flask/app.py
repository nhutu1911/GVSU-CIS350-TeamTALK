from flask import Flask
from flask import render_template

from markupsafe import escape


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/user/')
@app.route('/user/<name>')
def user(name=None):
    return render_template('user.html', name=name)

@app.route('/challenges/')
def challenges():
    return render_template('challenges.html')