from flask import current_app, Blueprint, request, jsonify
from models.user import User
from functools import wraps
import jwt
from datetime import datetime
from flask import current_app

reward_blueprint = Blueprint('reward', __name__)

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


@reward_blueprint.route('/details', methods=['GET'])
@token_required
def get_token(user, token):
    data = request.args
    print(data)

    return jsonify({'Hello Fresh - Protein Meals': 1,
                    'Fruit Juice Coupon 20%': 0})