from flask import Blueprint, jsonify, request
from models.user import User
from app import csrf
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required
from werkzeug.security import generate_password_hash

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
    return jsonify(user_array), 200

@users_api_blueprint.route('/<id>', methods=['GET'])
def showuser(id):
    user=User.get_or_none(User.id == id)
    if user:
        return jsonify({"id": user.id, "username": user.username,
                        "profileImage": user.profile_image_url}), 200
    else:
        return jsonify({"message": ["User does not exist"], "status": "failed"}), 404

@users_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def showme():
    username = get_jwt_identity()
    user = User.get_or_none(User.username == username)
    return jsonify({"id": user.id, "username": user.username,
                     "email": user.email,  "profile_picture": user.profile_image_url}), 200

@users_api_blueprint.route('/create', methods=['POST'])
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
    
@users_api_blueprint.route('/check_name', methods=['GET'])
def check_name():
    username = request.args.get('username')
    user = User.get_or_none(User.username == username)
    if user:
        return jsonify({"exists": True, "valid": False}), 200
    else:
        return jsonify({"exists": False, "valid": True}), 200






