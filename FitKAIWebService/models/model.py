from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    version_id = db.Column(db.String(50))
    algorithm_name = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_on = db.Column(db.DateTime)

class ModelLogs(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    version_id = db.Column(db.String(50))
    request_id = db.Column(db.String(200))
    response_id = db.Column(db.String(200))
    request_body = db.Column(db.JSON)
    response_body = db.Column(db.JSON)
    prediction_prob = db.Column(db.Float)
    prediction_label = db.Column(db.Integer)
    model = db.relationship('Model', backref=db.backref('model_logs', lazy=True))

class ModelMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    training_date = db.Column(db.DateTime)
    performance_metrics = db.Column(db.String(200))
    training_data = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_on = db.Column(db.DateTime)
    model = db.relationship('Model', backref=db.backref('model_metadata', lazy=True))

