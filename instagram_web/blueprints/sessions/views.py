from flask import Blueprint, render_template, request, redirect, url_for, flash, session, escape
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user
from app import app
from instagram_web.util.google_oauth import oauth

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
        flash(u"You are already logged in", 'info')
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
            flash(u"Login succesful", 'success')
            return redirect(url_for('home'))
        else:
            flash(u"Invalid password", 'warning')
            return redirect(url_for('sessions.new'))
    else:
        flash(u"Username does not exist!", 'warning')
        return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    flash(u"Succesfully logged out", 'success')
    return redirect(url_for('home'))

@sessions_blueprint.route('/google_login')
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google')
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash(u"Login successful", 'success')
        return redirect(url_for('home'))
    else:
        flash(u"You do not have an account. Please sign up", 'info')
        return redirect(url_for('users.new'))



