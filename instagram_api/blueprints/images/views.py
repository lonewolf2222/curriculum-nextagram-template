from flask import Blueprint, jsonify, request
from models.user import User
from models.image import Image
from flask_jwt_extended import jwt_required, get_jwt_identity

images_api_blueprint = Blueprint('images_api', __name__)

@images_api_blueprint.route('/images', methods=['GET'])
def index():
    user_id = request.args.get('userId')
    if user_id:
        images = Image.select().where(Image.user_id == user_id)
    else:
        images = Image.select()
    
    image_array = []
    for img in images:
        image_array.append(img.user_images_url)
    
    return jsonify(image_array)

# @images_api_blueprint.route('/images/protected', methods=['GET'])
# @jwt_required
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200

@images_api_blueprint.route('/images/me', methods=['GET'])
@jwt_required
def me():
    username = get_jwt_identity()
    user = User.get_or_none(User.username == username)
    images = Image.select().where(Image.user_id == user.id)
    return jsonify([img.user_images_url for img in images]), 200










