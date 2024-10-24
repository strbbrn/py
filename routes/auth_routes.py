from flask import Blueprint, request, jsonify, current_app
import hashlib
import jwt
import datetime
from db_operations import db_login, register_user
from flasgger import swag_from

auth_bp = Blueprint('auth', __name__)

@swag_from({
    'responses': {
        201: {'description': 'User registered successfully'},
        400: {'description': 'Error registering user'}
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'example': 'user@example.com'},
                    'password': {'type': 'string', 'example': 'password123'}
                }
            }
        }
    ]
})
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    register_user(data)
    return jsonify({'message': 'User registered successfully'}), 201

@swag_from({
    'responses': {
        200: {
            'description': 'Login successful',
            'examples': {'application/json': {'token': 'your-jwt-token-here'}}
        },
        401: {'description': 'Invalid credentials'}
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'example': 'user@example.com'},
                    'password': {'type': 'string', 'example': 'password123'}
                }
            }
        }
    ]
})
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
