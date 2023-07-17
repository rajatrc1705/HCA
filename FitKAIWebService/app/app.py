from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

db = SQLAlchemy()

def create_app():
    from routes.auth.routes import auth_blueprint
    from routes.analyzer.routes import analyzer_blueprint
    from routes.persistence.routes import persistence_blueprint
    from routes.user.routes import user_blueprint
    from routes.reward.routes import reward_blueprint
    from dotenv import load_dotenv
    load_dotenv()
    username = os.environ.get('DB_USERNAME')
    password = quote_plus(os.environ.get('DB_PASSWORD'))
    host = os.environ.get('HOST')
    port = os.environ.get('DB_PORT')
    dbname = os.environ.get('DB_NAME')
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@{host}:{port}/{dbname}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = "jasjkjajkjabjbsjxjaxkjsxkjbjkxbjkx"

    # organize routes
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(analyzer_blueprint, url_prefix='/analyzer')
    app.register_blueprint(persistence_blueprint, url_prefix='/persistence')
    app.register_blueprint(reward_blueprint, url_prefix='/reward')

    db.init_app(app)
    with app.app_context():
        # db.create_all()
        current_app.db = db
        current_app.Session = sessionmaker(bind=db.engine)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
