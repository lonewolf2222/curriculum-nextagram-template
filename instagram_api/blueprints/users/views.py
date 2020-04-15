from flask import Blueprint, jsonify, request
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()
    user_array = []
    for u in users:
        user_array.append({"id": u.id, "username": u.username,
                        "profileImage": u.profile_image_url})
    return jsonify(user_array)


