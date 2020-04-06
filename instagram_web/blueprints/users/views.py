from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import generate_password_hash
import re

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    username = username.strip()
    email = email.strip()
    password = password.strip()
    errors = []
    if not username:
        errors.append("Username cannot be empty")
    if not email:
        errors.append("Email cannot be empty")
    if ' ' in username:
        errors.append("Username must be one word")
    if len(password) < 6:
        errors.append("Password must be at least 6 characters")
    if re.search('[0-9]', password) is None:
        errors.append("Password must have at least one number")
    if re.search('[a-z]', password) is None:
        errors.append("Password must have at least one lower case letter")
    if re.search('[A-Z]', password) is None:
        errors.append("Password must have at least one capital letter")
    if re.search('[^A-Za-z\s0-9]', password) is None:
        errors.append("Password must have at least one special character")
    
    if len(errors) != 0:
        for e in errors:
            flash(e)
        return redirect(url_for('users.new'))
    else:
        hashed_password = generate_password_hash(password)
        user = User(username = username, password = hashed_password, email = email)
        if user.save():
            session['username'] = user.username
            flash("Your account has been created")
            return redirect(url_for('home'))
        else:
            errors = user.errors
            for e in errors:
                flash(e)
            return redirect(url_for('users.new'))

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
