from flask import Blueprint, request, jsonify
from persistence.services import register_workout, log_coordinates
from config.config import EXERCISE_MAPPING
from functools import wraps
import jwt
from datetime import datetime
from flask import current_app
from models.user import User

persistence_blueprint = Blueprint('persistence', __name__)

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

@persistence_blueprint.route('/user/<int:user_id>/workout', methods=['POST'])
@token_required
def post_stats(user, token, user_id):
    try:
        data = request.json
        #there should be an internal mapping of exercises and exercise_id
        exercise = data.get("exercise")
        exercise_id = EXERCISE_MAPPING.get(exercise)
        duration = data.get("duration")
        total_reps = data.get("total_reps")
        attempted_reps = data.get("attempted_reps")
        accuracy = (attempted_reps / total_reps) * 100

        register_workout(user_id, duration, exercise_id, total_reps, attempted_reps, accuracy)
    except Exception as e:
        return jsonify({
            "errorMsg": str(e)
        }), 500
    
    return jsonify(message='Workout registered successfully')

@persistence_blueprint.route('/user/<int:user_id>/logs', methods=['POST'])
@token_required
def logs(user, token, user_id):
    try:
        data = request.json
        #there should be an internal mapping of exercises and exercise_id
        exercise_id = data.get('exercise_id')
        coordinates = data.get("coordinates")
        
        log_coordinates(user_id, exercise_id, coordinates)
        pass
    except Exception as e:
        return jsonify({
            "errorMsg": str(e)
        }), 500
    
    return jsonify(message='Workout registered successfully')
    