from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3, allowed_file

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
            login_user(user)
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
@login_required
def edit(id):
    if str(current_user.id) == id:
        return render_template('users/edit.html')
    else:
        flash("You can only update your own details")
        return redirect(url_for('home'))


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    username = request.form.get('username')
    email = request.form.get('email')
    username = username.strip()
    email = email.strip()
    errors = []
    if not username and not email:
        errors.append("Nothing to update")
    if ' ' in username:
        errors.append("Username must be one word")

    if len(errors) != 0:
        for e in errors:
            flash(e)
        return redirect(url_for('users.edit', id=id))
    else:
        try:
            query = User.update(username=username, email=email).where(User.id == id)
            query.execute()
            flash("Details updated")
            return redirect(url_for('users.edit', id=id))
        except:
            flash("An error has occurred")
            return redirect(url_for('users.edit', id=id))

@users_blueprint.route('/<id>/passwd', methods=['GET'])
@login_required
def passwd(id):
    if current_user.id == id:
        return render_template('users/passwd.html')
    else:
        flash("You can only change your own password")
        return redirect(url_for('home'))

@users_blueprint.route('/passwd_update/<id>', methods=['POST'])
def passwd_update(id):
    oldpassword = request.form.get('oldpassword')
    newpassword = request.form.get('newpassword')
    oldpassword = oldpassword.strip()
    newpassword = newpassword.strip()
    user = User.get_or_none(User.id == id)

    errors = []
    if not check_password_hash(user.password, oldpassword):
        errors.append("Old password incorrect")
    if len(newpassword) < 6:
        errors.append("New Password must be at least 6 characters")
    if re.search('[0-9]', newpassword) is None:
        errors.append("New Password must have at least one number")
    if re.search('[a-z]', newpassword) is None:
        errors.append("New Password must have at least one lower case letter")
    if re.search('[A-Z]', newpassword) is None:
        errors.append("New Password must have at least one capital letter")
    if re.search('[^A-Za-z\s0-9]', newpassword) is None:
        errors.append("New Password must have at least one special character")

    if len(errors) != 0:
        for e in errors:
            flash(e)
        return redirect(url_for('users.passwd', id=id))
    else:
        hashed_password = generate_password_hash(newpassword)
        try:
            query = User.update(password=hashed_password).where(User.id == id)
            query.execute()
            flash("Password updated")
            return redirect(url_for('users.passwd', id=id))
        except:
            flash("An error has occurred")
            return redirect(url_for('users.passwd', id=id))

@users_blueprint.route('/upload/<id>', methods=['POST'])
def upload(id):
    # user = User.get_or_none(User.id == id)
    if "profile_image" not in request.files:
        flash("You must upload an image file")
        return redirect(url_for('users.edit', id=id))

    file = request.files["profile_image"]
    if file.filename == "":
        flash("Please select a file")
        return redirect(url_for('users.edit', id=id))

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        image = upload_file_to_s3(file)
        try:
            query = User.update(image_path=file.filename).where(User.id==id)
            query.execute()
            flash("Your profile picture is set!")
            return redirect(url_for('users.edit', id=id))
        except:
            flash("An error has occured. Please try again")
            return redirect(url_for('users.edit', id=id))
    else:
        flash("Unsupported file type")
        return redirect(url_for('users.edit', id=id))
