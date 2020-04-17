from flask import Blueprint, jsonify, request
from models.user import User
from models.image import Image
from flask_jwt_extended import jwt_required, get_jwt_identity
from instagram_web.util.helpers import upload_file_to_s3, allowed_file
from werkzeug.utils import secure_filename
import re

images_api_blueprint = Blueprint('images_api', __name__)

@images_api_blueprint.route('/', methods=['GET'])
def index():
    user_id = request.args.get('userId')
    if user_id:
        images = Image.select().where(Image.user_id == user_id)
    else:
        images = Image.select()
    
    image_array = []
    for img in images:
        image_array.append(img.user_images_url)
    
    return jsonify(image_array), 200

@images_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def me():
    username = get_jwt_identity()
    user = User.get_or_none(User.username == username)
    images = Image.select().where(Image.user_id == user.id)
    return jsonify([img.user_images_url for img in images]), 200

@images_api_blueprint.route('/upload', methods=['POST'])
@jwt_required
def upload_image():
    username = get_jwt_identity()
    user = User.get_or_none(User.username == username)

    if 'image' not in request.files:
        return jsonify({"message": "No image provided", "status":"failed"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"message": "No file selected for uploading", "status": "failed"}), 400
        
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        result = upload_file_to_s3(file)
        if re.search("http", str(result)):
            img = Image(image_path=file.filename, user_id=user.id)
            img.save()
            return jsonify({"image_url": "{user.user_images_url}", "success": True}), 200
        else:
            return jsonify({"message": "Network error. Try again", "status": "failed"}), 400       
    else:
        return jsonify({"message": "Unsupported file type", "status": "failed"}), 400

@images_api_blueprint.route('/profileimage', methods=['POST'])
@jwt_required
def profile_image():
    username = get_jwt_identity()
    user = User.get_or_none(User.username == username)

    if 'image' not in request.files:
        return jsonify({"message": "No image provided", "status":"failed"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"message": "No file selected for uploading", "status": "failed"}), 400
        
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        result = upload_file_to_s3(file)
        if re.search("http", str(result)):
            query = User.update(image_path=file.filename).where(User.id==user.id)
            query.execute()
            return jsonify({"image_url": "{user.profile_image_url}", "success": True}), 200
        else:
            return jsonify({"message": "Network error. Try again", "status": "failed"}), 400       
    else:
        return jsonify({"message": "Unsupported file type", "status": "failed"}), 400
