from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from app.app import db

class GoalType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'))
    goal = db.Column(db.Enum('lose_weight', 'gain', 'maintain'), nullable=False)
    
class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    birth_date = db.Column(db.DateTime)
    height = db.Column(db.Numeric(5, 2))
    weight = db.Column(db.Numeric(5, 2))
    goaltyperel = db.relationship('GoalType', backref='users')

    def __repr__(self):
        return f"UserDetails(id={self.user_id}, birth_date={self.birth_date}, goal_id={self.goal_id}, height={self.height})"
    