from flask import Flask
from flask_cors import CORS

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    from app.extensions import db
    from app.models.users import User
    from app.models.comments import Comment

    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Register blueprints here
    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    from app.comments import bp as comments_bp
    app.register_blueprint(comments_bp, url_prefix="/comments")

    return app
