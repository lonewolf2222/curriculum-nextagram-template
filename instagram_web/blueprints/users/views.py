from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models.image import Image
from models.follow import IdolFan
from werkzeug.security import generate_password_hash, check_password_hash
import re
from peewee import prefetch
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3, allowed_file, password_checker
from playhouse.flask_utils import object_list

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

    if len(errors) != 0:
        for e in errors:
            flash(e, 'warning')
        return redirect(url_for('users.new'))
    else:
        result = password_checker(password)
        if len(result) != 0:
            for e in result:
                flash(e, 'warning')
            return redirect(url_for('users.new'))
        else:
            hashed_password = generate_password_hash(password)
            user = User(username = username, password = hashed_password, email = email)
            if user.save():
                login_user(user)
                flash(u"Your account has been created", 'success')
                return redirect(url_for('home'))
            else:
                errors = user.errors
                for e in errors:
                    flash(e, 'warning')
                return redirect(url_for('users.new'))

@users_blueprint.route('/<username>/', methods=["GET"])
@login_required
def show(username):
    user = User.get_or_none(User.username == username)
    if not user:
        flash(u"User does not exist!",'warning')
        return redirect(url_for('home'))
    else:
        images = user.images
        if images:
            return object_list(
                '/users/show.html',
                query=images,
                context_variable='images_list',
                paginate_by=8,
                user=user)
        else:
            flash(f'{user.username} have no photo collection yet', 'info')
            return redirect(url_for('home'))
        # return render_template('users/show.html', user=user)

@users_blueprint.route('/', methods=["GET"])
def index():
    users = User.select()
    images = Image.select()
    users_with_images = prefetch(users, images)
    return render_template('users/index.html', users_with_images = users_with_images)

@users_blueprint.route('/<int:id>/edit', methods=['GET'])
@login_required
def edit(id):
    if (current_user.id) == id:
        return render_template('users/edit.html')
    else:
        flash(u"You can only update your own details!", 'danger')
        return redirect(url_for('home'))

@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    # user = User.get_or_none(User.id == id)
    username = request.form.get('username')
    email = request.form.get('email')
    username = username.strip()
    email = email.strip()
    status = request.form.get('status')
    if not username or not email:
        flash(u"Username and email cannot be empty", 'warning')
        return redirect(url_for('users.edit', id=id))
    if ' ' in username:
        flash(u"Username must be one word", 'warning')
        return redirect(url_for('users.edit', id=id))
    
    if status == None:
        private = False
    else:
        private = True
    try:
        query = User.update(username=username, email=email, private=private).where(User.id == id)
        query.execute()
        flash(u"Profile updated", 'info')
        return redirect(url_for('users.edit', id=id))
    except:
        flash(u"An error has occurred", 'warning')
        return redirect(url_for('users.edit', id=id))

@users_blueprint.route('/<int:id>/passwd', methods=['GET'])
@login_required
def passwd(id):
    if (current_user.id) == id:
        return render_template('users/passwd.html')
    else:
        flash(u"You can only change your own password", 'danger')
        return redirect(url_for('home'))

@users_blueprint.route('/passwd_update/<id>', methods=['POST'])
def passwd_update(id):
    oldpassword = request.form.get('oldpassword')
    newpassword = request.form.get('newpassword')
    oldpassword = oldpassword.strip()
    newpassword = newpassword.strip()
    user = User.get_or_none(User.id == id)

    if not check_password_hash(user.password, oldpassword):
        flash(u"Current password incorrect", 'warning')
        return redirect(url_for('users.passwd', id=id))
    else:
        result = password_checker(newpassword)
        if len(result) != 0:
            for e in result:
                flash(e)
            return redirect(url_for('users.passwd', id=id))
        else:
            hashed_password = generate_password_hash(newpassword)
            try:
                query = User.update(password=hashed_password).where(User.id == id)
                query.execute()
                flash(u"Password updated", 'info')
                return redirect(url_for('users.passwd', id=id))
            except:
                flash(u"An error has occurred", 'warning')
                return redirect(url_for('users.passwd', id=id))

@users_blueprint.route('/upload/<id>', methods=['POST'])
def upload(id):
    # user = User.get_or_none(User.id == id)
    if "profile_image" not in request.files:
        flash(u"You must upload an image file", 'warning')
        return redirect(url_for('users.edit', id=id))

    file = request.files["profile_image"]
    if file.filename == "":
        flash(u"Please select a file", 'warning')
        return redirect(url_for('users.edit', id=id))

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        result = upload_file_to_s3(file)
        if re.search("http", str(result)):
            try:
                query = User.update(image_path=file.filename).where(User.id==id)
                query.execute()
                flash(u"Profile picture updated!", 'success')
                return redirect(url_for('users.edit', id=id))
            except:
                flash(u"An error has occured. Please try again", 'warning')
                return redirect(url_for('users.edit', id=id))
        else: 
            flash(u"Network error has occured. Please try again", 'warning')
            return redirect(url_for('users.edit', id=id))
    else:
        flash(u"Unsupported file type", 'danger')
        return redirect(url_for('users.edit', id=id))

@users_blueprint.route('/search', methods=['GET'])
def search():
    search_username = request.args.get("username")
    return redirect(url_for('users.show', username=search_username))

@users_blueprint.route('/feed/', methods=['GET'])
@login_required
def feed():
    user = User.get_or_none(User.id == current_user.id)
    image_feed = user.image_feed
    if image_feed:
        return object_list(
            'users/feed.html',
            query=image_feed,
            context_variable='feed_list',
            paginate_by=8)
    else:
        flash(u'You have no image feed yet', 'info')
        return redirect(url_for('home'))


