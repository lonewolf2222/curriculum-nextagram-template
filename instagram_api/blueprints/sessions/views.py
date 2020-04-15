from flask import Blueprint, jsonify, request, make_response
from models.user import User
from werkzeug.security import check_password_hash

sessions_api_blueprint = Blueprint('sessions_api', __name__)

@sessions_api_blueprint.route('login', methods=['POST'])
def login():
    result = request.get_json()
    user = User.get_or_none(username=result.get('username'))
    password_correct = check_password_hash(user.password, result.get('password'))
    if user and password_correct:

        auth_token = user.encode_auth_token(user.id)

        responseObject = {
            'status': 'success',
            'message': 'Successfully signed in',
            'auth_token': auth_token.decode(),
            'user': {"id": user.id, "username": user.username, "profile_picture": user.profile_image_url}
        }
        return make_response(jsonify(responseObject)), 201
    
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Some error ocurred. Please try again'
        }
        return make_response(jsonify(responseObject)), 401

