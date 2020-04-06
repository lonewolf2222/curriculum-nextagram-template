from flask import Blueprint, render_template, request, redirect, url_for, flash, session, escape
from models.user import User
from werkzeug.security import check_password_hash

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    if 'username' in session:
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
            session["username"] = user.username
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
    session.pop('username', None)
    flash("Succesfully logged out")
    return redirect(url_for('home'))



