from flask import Flask, request, jsonify
from db_operations import get_all_students, get_student_by_id, create_student, update_student, delete_student, db_login, register_user
import jwt
import datetime
import hashlib
app = Flask(__name__)

app.config['SECRET_KEY'] = 'shashiadminkey'

def decode_token(token):
    if not token:
        return None, {'message': 'Auth Token is missing!'}

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return data['role'], None
    except jwt.ExpiredSignatureError:
        return None, {'message': 'Token has expired!'}
    except jwt.InvalidTokenError:
        return None, {'message': 'Invalid token!'}
    
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    register_user(data)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
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
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/students', methods=['GET'])
def get_students():
    students = get_all_students()
    if students:
        return jsonify(students)
    else:
        return jsonify({'message': 'Table empty'}), 404
    

@app.route('/students/<int:id>', methods=['GET'])
def get_user(id):
    user = get_student_by_id(id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/students', methods=['POST'])
def create_new_user():
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
    return jsonify({'message': 'User created successfully!'}), 201

@app.route('/students/<int:id>', methods=['PUT'])
def update_existing_user(id):
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
        return jsonify({'message': 'User updated successfully!'})
    else:
        return jsonify({'message': 'User not found'}), 404
    

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_existing_user(id):
    token = request.headers.get('access-token')
    role, error_response = decode_token(token)
    if error_response:
        return jsonify(error_response), 403

    if role != 'admin':
        return jsonify({'message': 'Permission denied: Admin role required'}), 403
    count = delete_student(id)
    if count == 1:
        return jsonify({'message': 'User deleted successfully!'})
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
