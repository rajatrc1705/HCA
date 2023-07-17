from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.preferences import UserDetails, GoalType
from flask import current_app
from datetime import datetime, timedelta
import jwt

def register_user(username, email, password):
    db = current_app.db
    # hashed_password = generate_password_hash(password)
    user = User(name=username, email=email, password=password)

    db.session.add(user)
    result = db.session.query(User).filter_by(email=email).first()
    db.session.commit()


def authenticate_user(username, password):
    #Session = sessionmaker(bind=current_app.db.engine)
    session = current_app.Session()

    user = session.query(User).filter_by(name=username).first()

    # if user and check_password_hash(user.password, password):
    if user and user.password == password:
        return user
    return None

def generate_jwt_token(user):
    # Generate JWT token using a secret key
    jwt_secret = current_app.config['JWT_SECRET_KEY']
    print(f"User: {user} - {user.id}")
    expiration_time = datetime.utcnow() + timedelta(minutes=10)
    expiration_time = expiration_time.timestamp()

    token_payload = {
        'user_id': user.id,
        'username': user.name,
        'expiration_time': expiration_time
    }

    token = jwt.encode(token_payload, jwt_secret, algorithm='HS256')
    return token
