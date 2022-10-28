from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('main.user'))
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('main.user'))
    return render_template('login.html')

@auth.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.index'))
