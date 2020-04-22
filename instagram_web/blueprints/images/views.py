from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.image import Image
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from instagram_web.util.helpers import upload_file_to_s3, allowed_file
import re

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')

@images_blueprint.route('/upload/<id>', methods=['POST'])
def upload(id):
    user = User.get_or_none(User.id == id)
    # profile_image = current_user.image_path
    if not current_user.image_path:
        flash(u"You must set a profile image first", 'danger')
        return redirect(url_for('users.edit', id=current_user.id))
    
    if "user_image" not in request.files:
        flash(u"You must upload an image file", 'warning')
        return redirect(url_for('images.new'))

    desc = request.form.get("desc")
    file = request.files["user_image"]
    if file.filename == "":
        flash(u"Please select a file", 'warning')
        return redirect(url_for('images.new'))

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        result = upload_file_to_s3(file)
        if re.search("http", str(result)):
            try:
                img = Image(image_path=file.filename, desc=desc, user_id=id)
                img.save()
                flash(u"Your Photo is uploaded!", 'success')
                return redirect(url_for('images.new'))
            except:
                flash(u"An error has occured. Please try again", 'warning')
                return redirect(url_for('images.new'))
        else: 
            flash(u"Network error. Please try again", 'warning')
            return redirect(url_for('images.new'))
    else:
        flash(u"Unsupported file type", 'danger')
        return redirect(url_for('images.new'))

@images_blueprint.route('/delete/<image_id>', methods=['GET'])
def delete(image_id):
    image_remove = Image.get_or_none(Image.id == image_id)
    try:
        image_remove.delete_instance()
        flash(u"Photo deleted", 'success')
        return redirect(url_for('users.show', username=current_user.username))
    except:
        flash(u"An error has occured. Please try again", 'warning')
        return redirect(url_for('users.show', username=current_user.username))

