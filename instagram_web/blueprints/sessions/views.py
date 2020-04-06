from flask import Blueprint, render_template, request, redirect, url_for, flash, session, escape
from models.user import User
from werkzeug.security import check_password_hash

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.get_or_none(User.username == username)

    if user:
        if check_password_hash(user.password, password):
            flash("Login succesful")
            return redirect(url_for('sessions.new'))
        else:
            flash("Invalid password")
            return redirect(url_for('sessions.new'))
    else:
        flash("Username does not exist!")
        return redirect(url_for('sessions.new'))

