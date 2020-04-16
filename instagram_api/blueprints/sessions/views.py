from flask import Blueprint, jsonify, request
from models.user import User
from app import app
import os
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

secret_key = os.environ.get("JWT_SECRET_KEY")
app.config['JWT_SECRET_KEY'] = secret_key
jwt = JWTManager(app)

sessions_api_blueprint = Blueprint('sessions_api', __name__)

@sessions_api_blueprint.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']
    user = User.get_or_none(username=username)
    password_check = check_password_hash(user.password, password)
    if user and password_check:

        access_token = create_access_token(identity=user.username)

        response = {
            'auth_token': access_token,
            'message': 'Successfully signed in',
            'status': 'success',
            'auth_token': access_token,
            'user': {"id": user.id, "username": user.username, "profile_picture": user.profile_image_url}
        }
        return jsonify(response), 201
    
    else:
        response = {
            'status': 'fail',
            'message': 'Some error ocurred. Please try again'
        }
        return jsonify(response), 401
