from flask import Blueprint, request, jsonify
from db_operations import get_all_students, get_student_by_id, create_student, update_student, delete_student
from utilis import decode_token

student_bp = Blueprint('student', __name__)


@student_bp.route('/', methods=['GET'])
def get_students():
    students = get_all_students()
    if students:
        return jsonify(students)
    return jsonify({'message': 'Table empty'}), 404


@student_bp.route('/<int:id>', methods=['GET'])
def get_student(id):
    student = get_student_by_id(id)
    if student:
        return jsonify(student)
    return jsonify({'message': 'Student not found'}), 404


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
