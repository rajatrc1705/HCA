
from flask import current_app, Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from auth.services import register_user, authenticate_user, generate_jwt_token
from models.user import User
from functools import wraps
from datetime import datetime
import jwt

auth_blueprint = Blueprint('auth', __name__)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        data = jwt.decode(
            token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        current_user = User.query.filter_by(name=data['username']).first()
        
        # checks if token is expired
        is_token_valid = datetime.utcnow(
        ).timestamp() < data['expiration_time']
        
        # checks if token is already blacklisted or not

        with open('..\\..\\blacklisted_tokens.txt', 'r') as file:
            blacklisted_tokens = file.read()
        blacklisted_tokens = blacklisted_tokens.split(',\n')
        is_token_valid = True if token not in blacklisted_tokens else False

        if is_token_valid:
            return f(current_user, token, *args, **kwargs)
        else:
            return jsonify({'message': 'expired token, please log in to the system'})
    return decorator


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    print(f"Data: {data}")
    register_user(username, email, password)
    return jsonify(message='User registered successfully')


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = authenticate_user(username, password)
    if user:
        # Generate JWT token and return it to the client
        token = generate_jwt_token(user)
        return jsonify({
            'user_id': user.id,
            'token':token
            })
    else:
        return jsonify(error='Invalid credentials'), 401


@auth_blueprint.route('/logout', methods=['GET'])
@token_required
def logout(user, token):
    
    file_path = '..\\..\\blacklisted_tokens.txt'

    with open(file_path, 'a') as file:
        file.write(token + ',\n')

    return jsonify({
        'error': 'Logout successful',
        'token': token
    })
