from flask import Blueprint, render_template, request, redirect, url_for, flash, session, escape
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user
from app import app

login_manager = LoginManager()
login_manager.init_app(app)

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    if current_user.is_authenticated:
        flash("You are already logged in")
        return redirect(url_for('home'))
    else:
        return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    password = request.form.get('password')
    username = username.strip()
    password = password.strip()
    user = User.get_or_none(User.username == username)

    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            flash("Login succesful")
            return redirect(url_for('home'))
        else:
            flash("Invalid password")
            return redirect(url_for('sessions.new'))
    else:
        flash("Username does not exist!")
        return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    flash("Succesfully logged out")
    return redirect(url_for('home'))



