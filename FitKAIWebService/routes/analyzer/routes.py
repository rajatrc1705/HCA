from flask import Blueprint, request, jsonify
from analyzer.services import get_user_stats, get_user_workout_progress
from datetime import datetime, timedelta
from config.config import EXERCISE_MAPPING
from functools import wraps
import jwt
from datetime import datetime
from flask import current_app
from models.user import User

analyzer_blueprint = Blueprint('analyzer', __name__)

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


# routes.py
@analyzer_blueprint.route('/user/<int:user_id>/stats', methods=['GET'])
@token_required
def get_stats(user, token, user_id):
    try:
        stats = get_user_stats(user_id)
        return jsonify(stats)
    except Exception as e:
        return jsonify({
            "errorMsg": str(e)
        }), 500
    
@analyzer_blueprint.route('/user/<int:user_id>/workout-progress', methods=['GET'])
@token_required
def get_workout_progress(user, token, user_id):
    try:
        exercise = request.args.get('exercise')
        exercise_id = EXERCISE_MAPPING.get(exercise)
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        if exercise_id is None or start_date_str is None or end_date_str is None:
            raise ValueError('Invalid Exercise id.')
    except Exception as e:
        return jsonify(error='Invalid request.Please check your parameters again.'), 400


    # Validate and parse the start and end dates
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify(error='Invalid date format'), 400

    end_date = end_date + timedelta(days=1)

    try:
        formatted_data = get_user_workout_progress(user_id,exercise_id,start_date,end_date)
        print(formatted_data)
    except Exception as e:
        return jsonify(error=str(e)), 400

    return jsonify(workout_progress=formatted_data)