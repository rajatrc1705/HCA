# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# from flask import current_app
# from app.app import db

# #db = SQLAlchemy()

# class Workout(db.Model):
#     __tablename__ = 'workout'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
#     duration = db.Column(db.String(20))
#     total_reps = db.Column(db.Integer)
#     attempted_reps = db.Column(db.Integer)
#     accuracy = db.Column(db.Float)
#     workout_datetime = db.Column(db.DateTime, default=datetime.utcnow)
#     created_on = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_on = db.Column(db.DateTime, default=datetime.utcnow)
#     deleted_on = db.Column(db.DateTime)
#     # user = db.relationship('User', backref="workout", lazy=True)
#     # exercise = db.relationship('Exercise', backref='workout', lazy=True)