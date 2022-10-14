from flask import Flask
from flask import render_template

from markupsafe import escape


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/user/')
@app.route('/user/<name>')
def user(name=None):
    return render_template('user.html', name=name)