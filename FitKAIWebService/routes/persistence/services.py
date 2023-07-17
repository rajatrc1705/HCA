from flask import current_app, jsonify
from models.exercise import Workout

def register_workout(user_id, duration,exercise_id,total_reps, attempted_reps, accuracy):
    try:
        session = current_app.Session()
        workout = Workout(user_id=user_id,exercise_id=exercise_id, duration=duration, total_reps=total_reps, attempted_reps=attempted_reps, accuracy=accuracy)
        session.add(workout)
        session.commit()
        session.close()
    except Exception as e:
        raise e
import os    
def log_coordinates(user_id, exercise_id, coordinates):
    try:
        print(os.getcwd())
        final_string = f'{user_id},{exercise_id},{coordinates}'
        with open(f'..\\logs\\{user_id}\\coordinates.csv', 'a') as file:
            file.write(final_string+'\n')
    except Exception as e:
        raise e