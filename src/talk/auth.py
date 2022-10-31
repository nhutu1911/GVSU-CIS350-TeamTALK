from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import Blueprint

from flask_login import login_required, logout_user, current_user, login_user
from .forms import LoginForm, RegisterForm
from .models import db, User
from . import login_manager


auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print('User found')
            if user.check_password(form.password.data):
                print('Password correct')
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(url_for('main.user'))
        # flash('Invalid username/password combination')
        return redirect(url_for('auth.login'))
    return render_template('login.html', form=form)

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            user = User(username=form.username.data, points=0)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for('main.user'))
    return render_template('register.html', form=form)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    #flash("You must be logged in to view that page.")
    return redirect(url_for("auth.login"))

@auth.route('/admin/')
@login_required
def admin():
    if current_user.username == 'admin':
        users = User.query.all()
        return render_template('admin.html', users=users)
    return redirect(url_for('main.index'))

@auth.route('/admin/delete/', methods=['POST'])
@login_required
def delete_user():
    if current_user.username == 'admin':
        user = User.query.get(request.form['id'])
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('auth.admin'))
    return redirect(url_for('main.index'))

@auth.route('/admin/setpoints/', methods=['POST'])
@login_required
def set_points():
    if current_user.username == 'admin':
        print(request.form)
        user = User.query.get(request.form['id'])
        user.set_points(request.form['points'])
        db.session.commit()
        return redirect(url_for('auth.admin'))
    return redirect(url_for('main.index'))
