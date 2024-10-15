from flask import Flask, request, jsonify
from db_operations import get_all_students, get_student_by_id, create_student, update_student, delete_student

app = Flask(__name__)

@app.route('/students', methods=['GET'])
def get_students():
    students = get_all_students()
    return jsonify(students)

@app.route('/students/<int:id>', methods=['GET'])
def get_user(id):
    user = get_student_by_id(id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/students', methods=['POST'])
def create_new_user():
    data = request.json
    name = data['name']
    email = data['email']
    create_student(name, email)
    return jsonify({'message': 'User created successfully!'}), 201

@app.route('/students/<int:id>', methods=['PUT'])
def update_existing_user(id):
    data = request.json
    name = data['name']
    email = data['email']
    update_student(id, name, email)
    return jsonify({'message': 'User updated successfully!'})

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_existing_user(id):
    delete_student(id)
    return jsonify({'message': 'User deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
