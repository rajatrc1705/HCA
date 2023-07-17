from models.user import User
from flask import current_app


def update_user(username, email, password):

    db = current_app.db
    user = db.session.query(User).filter_by(email=email).first()
    if user:
        user.name = username  # Update the desired attribute
        db.session.commit()  # Commit the changes
        return True
    else:
        return False
    
def update_user_preferences(id, birth_date, height, weight, goal):

    db = current_app.db
    user = db.session.query(User).filter_by(id=id).first()

    if user and goal in ['gain', 'maintain', 'lose_weight']:
        user.birth_date = birth_date
        user.height = height
        user.weight = weight
        user.goal = goal
        db.session.commit()
        return True
    else:
        return False