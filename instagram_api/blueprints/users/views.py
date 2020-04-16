from flask import Blueprint, jsonify, request
from models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')


@users_api_blueprint.route('/users', methods=['GET'])
def index():
    users = User.select()
    user_array = []
    for u in users:
        user_array.append({"id": u.id, "username": u.username,
                        "profileImage": u.profile_image_url})
    return jsonify(user_array)

@users_api_blueprint.route('/users', methods=['POST'])
def create():
    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']
    email = req_data['email']

    if not username or not password or not email:
        return jsonify({"message": ["All fields are required!"], "status": "failed"}), 400
    
    hashed_password = generate_password_hash(password)
    username_check = User.get_or_none(User.username == username)
    email_check = User.get_or_none(User.email == email)
    if not username_check and not email_check:
        u = User(username=username, email=email, password=hashed_password)
        u.save()
        user = User.get(User.username == username)

        access_token = create_access_token(identity=username)

        response = {
            'auth_token': access_token,
            'message': 'Successfully signed in',
            'status': 'success',
            'auth_token': access_token,
            'user': {"id": user.id, "username": user.username, "profile_picture": user.profile_image_url}
        }
        return jsonify(response), 201

    else:
        return jsonify({"message": ["Username or email already in use"], "status": "failed"}), 400






