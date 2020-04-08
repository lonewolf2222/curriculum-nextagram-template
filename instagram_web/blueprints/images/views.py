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
    # user = User.get_or_none(User.id == id)
    desc = request.form.get("desc")
    if "user_image" not in request.files:
        flash("You must upload an image file")
        return redirect(url_for('images.new'))

    file = request.files["user_image"]
    if file.filename == "":
        flash("Please select a file")
        return redirect(url_for('images.new'))

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        result = upload_file_to_s3(file)
        if re.search("http", str(result)):
            try:
                img = Image(image_path=file.filename, desc=desc, user_id=id)
                img.save()
                flash("Your Photo is uploaded!")
                return redirect(url_for('home'))
            except:
                flash("An error has occured. Please try again")
                return redirect(url_for('images.new'))
        else: 
            flash("Network error. Please try again")
            return redirect(url_for('images.new'))
    else:
        flash("Unsupported file type")
        return redirect(url_for('images.new'))