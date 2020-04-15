from flask import Blueprint, jsonify, request
from models.user import User
from models.image import Image


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
    
    return jsonify(image_array)