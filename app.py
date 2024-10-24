from flask import Flask, request
import jwt
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'shashiadminkey'
app.config['SWAGGER'] = {
    'title': 'Student API',
    'uiversion': 3
}
swagger = Swagger(app)

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

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(student_bp, url_prefix='/students')

if __name__ == '__main__':
    app.run(debug=True)
