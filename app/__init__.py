from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    from app.database import db
    from app.marshmallow import marshmallow
    
    from app.models.users import User
    from app.models.comments import Comment
    
    db.init_app(app)
    marshmallow.init_app(app)
    migrate = Migrate(app, db)
    
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()
    
    # Register blueprints here
    from app.blueprints.users_blueprint import users_blueprint
    from app.blueprints.comments_blueprint import comments_blueprint
    
    app.register_blueprint(users_blueprint, url_prefix="/users")
    app.register_blueprint(comments_blueprint, url_prefix="/comments")
    
    # Initialize Swagger
    from app.docs import initialize_swagger
    initialize_swagger(app)

    return app
