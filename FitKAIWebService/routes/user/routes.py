from flask import current_app, Blueprint, request, jsonify
from models.user import User
from user.services import update_user, update_user_preferences
from functools import wraps
import jwt
from datetime import datetime, timedelta
from flask import current_app
import os

user_blueprint = Blueprint('user', __name__)

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

@user_blueprint.route('/details', methods=['GET'])
@token_required
def details(user, token):

    data = request.args
    db = current_app.db
    print(f"\n\n Name of User Received: {user.name}\n\n")
    results = db.session.query(User).filter_by(id=data['user_id']).first()
    if results is not None:
        return jsonify({
            'name': results.name,
            'email': results.email,
            'birth_date': results.birth_date,
            'height': results.height,
            'weight': results.weight,
            'goal': results.goal
        })
    else:
        return jsonify(message=f'No User Found {-1}')


@user_blueprint.route('/update', methods=['POST'])
@token_required
def update(user, token):

    data = request.json

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    update_result = update_user(username, email, password)
    if update_result:
        return jsonify(message='User Details updated successfully')
    else:
        return jsonify(message='Update Failed!')


@user_blueprint.route('/update/preferences', methods=['POST'])
@token_required
def update_preferences(user, token):

    data = request.json
    id = data.get('id')
    birth_date = data.get('birth_date')
    height = data.get('height')
    weight = data.get('weight')
    goal = data.get('goal')
    update_result = update_user_preferences(
        id, birth_date, height, weight, goal)
    if update_result:
        return jsonify(message='User Details updated successfully')
    else:
        return jsonify(message='Update Failed!')