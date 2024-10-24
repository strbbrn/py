from flask import Blueprint, request, jsonify
from db_operations import get_all_students, get_student_by_id, create_student, update_student, delete_student
from utilis import decode_token
from flasgger import swag_from

student_bp = Blueprint('student', __name__)

@swag_from({
    'responses': {
        200: {
            'description': 'List of all students',
            'examples': {
                'application/json': [
                    {'id': 1, 'name': 'Shashi', 'email': 'kumar@gmail.com'},
                    {'id': 2, 'name': 'Shashi', 'email': 'kumar@gmail.com'}
                ]
            }
        },
        404: {'description': 'No students found'}
    }
})
@student_bp.route('/', methods=['GET'])
def get_students():
    students = get_all_students()
    if students:
        return jsonify(students)
    return jsonify({'message': 'No students found'}), 404

@swag_from({
    'responses': {
        200: {
            'description': 'Student details',
            'examples': {
                'application/json': {
                    'id': 1,
                    'name': 'John Doe',
                    'email': 'john@example.com'
                }
            }
        },
        404: {'description': 'Student not found'}
    },
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'The ID of the student'
        }
    ]
})
@student_bp.route('/<int:id>', methods=['GET'])
def get_student(id):
    student = get_student_by_id(id)
    if student:
        return jsonify(student)
    return jsonify({'message': 'Student not found'}), 404

@swag_from({
    'responses': {
        201: {'description': 'Student created successfully'},
        403: {'description': 'Permission denied: Admin role required'}
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'Shashi Kumar'},
                    'email': {'type': 'string', 'example': 'kumar@gmail.com'}
                }
            }
        },
        {
            'name': 'access-token',
            'in': 'header',
            'required': True,
            'type': 'string',
            'description': 'JWT access token for authentication'
        }
    ]
})
@student_bp.route('/', methods=['POST'])
def create_new_student():
    token = request.headers.get('access-token')
    role, error_response = decode_token(token)
    if error_response:
        return jsonify(error_response), 403

    if role != 'admin':
        return jsonify({'message': 'Permission denied: Admin role required'}), 403

    data = request.json
    name = data['name']
    email = data['email']
    create_student(name, email)
    return jsonify({'message': 'Student created successfully!'}), 201

@swag_from({
    'responses': {
        200: {'description': 'Student updated successfully'},
        404: {'description': 'Student not found'},
        403: {'description': 'Permission denied: Admin role required'}
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'Shashi Kumar'},
                    'email': {'type': 'string', 'example': 'kumar@gmail.com'}
                }
            }
        },
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'The ID of the student to update'
        },
        {
            'name': 'access-token',
            'in': 'header',
            'required': True,
            'type': 'string',
            'description': 'JWT access token for authentication'
        }
    ]
})
@student_bp.route('/<int:id>', methods=['PUT'])
def update_student_info(id):
    token = request.headers.get('access-token')
    role, error_response = decode_token(token)
    if error_response:
        return jsonify(error_response), 403

    if role != 'admin':
        return jsonify({'message': 'Permission denied: Admin role required'}), 403

    data = request.json
    name = data['name']
    email = data['email']
    count = update_student(id, name, email)
    if count == 1:
        return jsonify({'message': 'Student updated successfully!'})
    return jsonify({'message': 'Student not found'}), 404

@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'The ID of the student to delete'
        },
        {
            'name': 'access-token',
            'in': 'header',
            'required': True,
            'type': 'string',
            'description': 'JWT access token for authentication'
        }
    ],
    'responses': {
        200: {'description': 'Student deleted successfully'},
        404: {'description': 'Student not found'},
        403: {'description': 'Permission denied: Admin role required'}
    }
})
@student_bp.route('/<int:id>', methods=['DELETE'])
def delete_student_info(id):
    token = request.headers.get('access-token')
    role, error_response = decode_token(token)
    if error_response:
        return jsonify(error_response), 403

    if role != 'admin':
        return jsonify({'message': 'Permission denied: Admin role required'}), 403

    count = delete_student(id)
    if count == 1:
        return jsonify({'message': 'Student deleted successfully!'})
    return jsonify({'message': 'Student not found'}), 404
