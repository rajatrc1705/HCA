from flask import current_app, jsonify
from models.exercise import Workout
from datetime import datetime, timedelta
import json
from sqlalchemy import func, text

def get_workouts_for_user(user_id):
    try:
        session = current_app.Session()
        workouts = session.query(Workout).filter_by(user_id=user_id).all()
        session.close()
    except Exception as e:
        raise e
    return workouts

def parse_duration_str(duration_str):
    # Parse the duration string
    try:
        duration_obj = datetime.strptime(duration_str, "%H:%M:%S")

        # Calculate the total duration in seconds
        duration_mins = timedelta(hours=duration_obj.hour, minutes=duration_obj.minute, seconds=duration_obj.second).total_seconds()/60

        # Convert to integer duration
        duration_int = int(duration_mins)
    except Exception as e:
        raise e

    return duration_int


def get_user_stats(user_id):

    try:
        workouts = get_workouts_for_user(user_id)
    
        total_workouts = len(workouts)
        total_duration = sum(parse_duration_str(workout.duration) for workout in workouts)
        avg_duration = total_duration / total_workouts if total_workouts else 0
        
        total_reps = sum(workout.total_reps for workout in workouts)
        avg_reps = total_reps / total_workouts if total_workouts else 0
        
        total_exercises = len(set(workout.exercise_id for workout in workouts))
        
        avg_accuracy = sum(workout.accuracy for workout in workouts) / total_workouts if total_workouts else 0
    
    except Exception as e:
        raise e

    return {
        "total_workouts": total_workouts,
        "total_duration": total_duration,
        "avg_duration": avg_duration,
        "total_reps": total_reps,
        "avg_reps": avg_reps,
        "total_exercises": total_exercises,
        "avg_accuracy": avg_accuracy,
    }

def get_user_workout_progress(user_id, exercise_id, start_date, end_date):
    try:
        session = current_app.Session()
        workout_data = (
            session.query(
                func.DATE_FORMAT(Workout.workout_datetime, '%Y-%m-%d').label('date'),
                func.avg(Workout.accuracy).label('average_accuracy')
            )
            .filter(
                Workout.user_id == user_id,
                Workout.exercise_id == exercise_id,
                Workout.workout_datetime >= start_date,
                Workout.workout_datetime <= end_date
            )
            .group_by(text("DATE_FORMAT(workout_datetime, '%Y-%m-%d')"))
            .order_by(text("DATE_FORMAT(workout_datetime, '%Y-%m-%d')"))
            .all()
        )

        # Format the query result into a list of dictionaries
        formatted_data = [
            {'date': row[0], 'average_accuracy': row[1]}
            for row in workout_data
        ]
        print(formatted_data)

        return formatted_data
    except Exception as e:
        raise e
