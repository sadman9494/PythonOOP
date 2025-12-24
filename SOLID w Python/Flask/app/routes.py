from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.model import get_user_by_username

auth_bp = Blueprint('auth', __name__)
api_bp = Blueprint('api', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('userName')  
    password = data.get('password')

    user = get_user_by_username(username)

    if not user or user['password'] != password:
        return jsonify({'msg': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
