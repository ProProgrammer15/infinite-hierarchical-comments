from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.users import User
from app.database import db
from app.marshmallow import ValidationError
from app.schemas.user_schema import UserSchema

users_blueprint = Blueprint("users", __name__)
user_schema = UserSchema()


@users_blueprint.route("/login", methods=["POST"])
def login_user():
    """It validates the user credentials i.e (username and password or email and password),
    checks if any user exists against the following credentials and add user to the session.
    If the user selects the remember me check, then he will be remained login 
    for 30 days

    Returns:
        _type_: Login success or failure message as json
    """
    try:
        # Deserialize request JSON (validate username/email and password)
        data = user_schema.load(request.json, partial=("username", "email"))
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter((User.username == username) | (User.email == email)).first()
    
    if not user:
        return jsonify({"error": "No user found"}), 400

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Incorrect password"}), 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    user_details = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
    
    return jsonify({"access_token": access_token, "refresh_token": refresh_token, "user": user_details})

    
@users_blueprint.route("/signup", methods=["POST"])
def signup_user():
    """It takes the user credentials (username, email and password), validates them
    and creates a new user if the user with the following credentials doesn't exists.

    Raises:
        e: If adding a new user to the database failes, exception will be raised

    Returns:
        _type_: User registration success or failure message
    """
    try:
        # Validate input and load data
        data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if User.query.filter_by(username=data["username"]).first() or \
       User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Username or email already exists"}), 400

    hashed_password = generate_password_hash(data["password"])
    new_user = User(username=data["username"], email=data["email"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": "User created successfully"})
    

@users_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """Refreshes the access token

    Returns:
        _type_: access_token
    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)
