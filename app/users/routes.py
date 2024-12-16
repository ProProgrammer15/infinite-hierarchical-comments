import json

from flask import request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

from app.users import bp
from app.models.users import User
from app.extensions import db
from app.utils.user_validations import (
    is_valid_email,
    is_valid_username,
    is_valid_password
)


@bp.route("/login", methods=["POST"])
def login_user():
    """It validates the user credentials i.e (username and password or email and password),
    checks if any user exists against the following credentials and add user to the session.
    If the user selects the remember me check, then he will be remained login 
    for 30 days

    Returns:
        _type_: Login success or failure message as json
    """
    request_data = json.loads(request.data)
    
    username = request_data.get("username", None)
    email = request_data.get("email", None)
    password = request_data.get("password", None)
    remember_me = request_data.get("remember_me", False)
    
    if not username or email:
        return jsonify({"error": "Username or email is required to login"}), 400
    
    if not password:
        return jsonify({"error": "Password is required to login"}), 400
        
    if username:
        user = db.session.query(User).filter_by(username=username).first()
    else:
        user = db.session.query(User).filter_by(email=email).first()
    
    if not user:
        return jsonify({"error": "No user exists"}), 400
    
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Incorrect password"}), 400
    
    if remember_me:
        session.permanent = True
    
    session["user_id"] = user.id
    
    return jsonify({"success": "Logged in successfully"})


@bp.route("/signup", methods=["POST"])
def signup_user():
    """It takes the user credentials (username, email and password), validates them
    and creates a new user if the user with the following credentials doesn't exists.

    Raises:
        e: If adding a new user to the database failes, exception will be raised

    Returns:
        _type_: User registration success or failure message
    """
    request_data = json.loads(request.data)
    
    username = request_data.get("username", None)
    email = request_data.get("email", None)
    password = request_data.get("password", None)
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    if not is_valid_username(username):
        return jsonify({"error": "Username must be alphanumeric and between 5 and 20 characters"}), 400
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400
    
    if not password:
        return jsonify({"error": "Password is required"}), 400
    
    if not is_valid_password(password):
        return jsonify({"error": "Password must be 8-20 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character"}), 400
    
    user_exists = db.session.query(User).filter(or_(User.username == username, User.email == email)).first() is not None
    
    if user_exists:
        return jsonify({"error": "User with this email or username already exists"}), 400
    
    try:
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        raise e
    
    return jsonify({"success": "User created successfully"})
