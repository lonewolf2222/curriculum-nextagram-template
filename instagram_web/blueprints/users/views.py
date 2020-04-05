from flask import Blueprint, render_template, request, redirect, url_for, flash
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
    if not username:
        flash("Username cannot be empty")
        return redirect(url_for('users.new'))
    if not email:
        flash("Email cannot be empty")
        return redirect(url_for('users.new'))
    if len(password) < 6:
        flash("Password must be at least 6 characters")
        return redirect(url_for('users.new'))
    if re.search('[0-9]', password) is None:
        flash("Password must have at least one number")
        return redirect(url_for('users.new'))
    if re.search('[A-Z]', password) is None:
        flash("Password must have at least one capital letter")
        return redirect(url_for('users.new'))
    if re.search('[^A-Za-z\s0-9]', password) is None:
        flash("Password must have at least one special character")
        return redirect(url_for('users.new'))

    hashed_password = generate_password_hash(password)
    user = User(username = username, password = hashed_password, email = email)
    if user.save():
        flash("Your account has been created")
        return redirect(url_for('users.new'))
    else:
        return render_template('users/new.html', errors=user.errors)

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
