from datetime import datetime
from app.app import db

#db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.DateTime)
    height = db.Column(db.Numeric(5, 2))
    weight = db.Column(db.Numeric(5, 2))
    goal = db.Column(db.Enum('lose_weight', 'gain', 'maintain'), nullable=False, default='maintain')
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime)
    deleted_on = db.Column(db.DateTime)
    user = db.relationship('Workout', backref="user", lazy=True, uselist=False)