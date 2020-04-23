from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user
from app import app
from instagram_web.util.google_oauth import oauth
from instagram_web.util.facebook_oauth import facebook_oauth
from instagram_web.util.helpers import password_checker
from instagram_web.util.sendmail import send_email_reset
import jwt
from time import time
from instagram_web.util.helpers import is_safe_url

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sessions.new"
login_manager.login_message_category = "info"

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        session['next_url'] = request.args.get('next')
        return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    password = request.form.get('password')
    # next_url = request.form.get('next')
    username = username.strip()
    password = password.strip()
    user = User.get_or_none(User.username == username)

    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            flash(u"Log In Successful", 'success')
            return redirect(url_for('sessions.check_redirect'))
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

@sessions_blueprint.route("/check_redirect")
def check_redirect():
    if session.get('next_url'):
        next_url = session.get('next_url')
        session.pop('next_url', None)
        if not is_safe_url(next_url):
            return abort(400)
        return redirect(next_url)
    return redirect(url_for('users.index'))

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
        return redirect(url_for('sessions.check_redirect'))
    else:
        flash(u"You do not have an account. Please sign up", 'info')
        return redirect(url_for('users.new'))

@sessions_blueprint.route('/forgot_password', methods=['GET'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if session.get('saved_email'):
        session.pop('saved_email', None)  # always clear session saved_email first
    return render_template('sessions/forgot.html')

@sessions_blueprint.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    user = User.get_or_none(User.email == email)
    if user:
        reset_token = jwt.encode({'email': user.email, 'exp': time()+600}, app.config['SECRET_KEY']).decode('utf-8')
        try:
            send_email_reset(receiver_email=email, reset_token=reset_token)
            flash(u"An email with instructions have been sent to your Inbox", 'info')
            return redirect(url_for('home'))
        except:
            flash(u"An error have occured. Please try again", 'warning')
            return redirect(url_for('sessions.forgot_password'))
    else:
        flash(u"Email does not exist", 'warning')
        return redirect(url_for('sessions.forgot_password'))

@sessions_blueprint.route('/verify_token/<reset_token>', methods=['GET'])
def verify_token(reset_token): 
    if session.get('saved_email'):   # check if any pending password reset
        flash(u"You can only reset one password at a time", 'danger')
        return redirect(url_for('home'))
    try:
        email = jwt.decode(reset_token, app.config['SECRET_KEY'])['email']
        session['saved_email'] = email # set saved_email session
        user = User.get_or_none(User.email == email)
        if user:
            flash(u"Please set your new password", 'info')
            return render_template('sessions/newpassword.html', email=email)
        else:
            flash(u"Invalid user", 'warning')
            return redirect(url_for('sessions.forgot_password'))
    except:
        flash(u"Invalid or expired token!", 'warning')
        return redirect(url_for('sessions.forgot_password'))

@sessions_blueprint.route('/new_password', methods=['POST'])
def new_password():
    email = request.form.get('email')
    new_password = request.form.get('newpassword')
    result = password_checker(new_password)
    if len(result) != 0:
        saved_email = session.get('saved_email')
        for e in result:
            flash(e, 'warning')
        flash("Please try again", 'info')
        return render_template('sessions/newpassword.html', email=saved_email)
    hashed_password = generate_password_hash(new_password)
    try:
        query = User.update(password=hashed_password).where(User.email == email)
        query.execute()
        session.pop('saved_email', None)  # clear the saved_email session
        flash(u"Password updated", 'info')
        return redirect(url_for('sessions.new'))
    except:
        session.pop('saved_email', None)
        flash(u"An error has occurred", 'warning')
        return redirect(url_for('sessions.forgot_password'))

@sessions_blueprint.route('/facebook_login', methods=['GET'])
def facebook_login():
    redirect_uri = url_for('sessions.facebook_authorize', _external=True )
    return facebook_oauth.facebook.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/facebook', methods=['GET'])
def facebook_authorize():
    try:
        facebook_oauth.facebook.authorize_access_token()
        facebook_user_data = facebook_oauth.facebook.get(
            "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
        ).json()

        email = facebook_user_data["email"]
        user = User.get_or_none(User.email == email)
        if user:
            login_user(user)
            flash(u"Login successful", 'success')
            return redirect(url_for('sessions.check_redirect'))
        else:
            flash(u"You do not have an account. Please sign up", 'info')
            return redirect(url_for('users.new'))
    except:
        flash(u"Login canceled", 'warning')
        return redirect(url_for('sessions.new'))








