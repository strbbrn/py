from flask import Flask, request, jsonify
from models import db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/shashi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/students', methods=['GET'])
def get_students():
    students = User.query.all()
    return jsonify([user.to_dict() for user in students])

@app.route('/students/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict())
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/students', methods=['POST'])
def create_user():
    data = request.json
    name = data['name']
    email = data['email']
    
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully!'}), 201

@app.route('/students/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    
    if user:
        user.name = data['name']
        user.email = data['email']
        db.session.commit()
        return jsonify({'message': 'User updated successfully!'})
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully!'})
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
