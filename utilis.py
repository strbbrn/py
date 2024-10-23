import jwt
from flask import current_app

def decode_token(token):
    if not token:
        return None, {'message': 'Auth Token is missing!'}

    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return data['role'], None
    except jwt.ExpiredSignatureError:
        return None, {'message': 'Token has expired!'}
    except jwt.InvalidTokenError:
        return None, {'message': 'Invalid token!'}
