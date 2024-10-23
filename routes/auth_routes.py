from flask import Blueprint, request, jsonify, current_app
import hashlib
import jwt
import datetime
from db_operations import db_login, register_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    register_user(data)
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    auth_data = request.get_json()
    email = auth_data['email']
    password = auth_data['password']
    user = db_login(email)

    if user and hashlib.md5(password.encode()).hexdigest() == user['password']:
        token = jwt.encode({
            'user': email,
            'role': user['role'],
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials'}), 401
