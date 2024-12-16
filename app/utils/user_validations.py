from flask import jsonify
import re


def is_valid_email(email):
    """It validates that email should be in the correct email format. 
    Args:
        email (string): Email input from the user

    Returns:
        _type_: Boolean to indicate if email format is valid or not
    """
    # Regex for validating email
    email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def is_valid_password(password):
    """It validates that password should be between 8 and 20 characters, and 
    must contains alphabets, numbers, and special characters

    Args:
        password (string): Password input from the user

    Returns:
        _type_: Boolean to indicate that if password is in required format
    """
    return (
        len(password) >= 8 and
        len(password) <= 20 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )

def is_valid_username(username):
    """It validates that username must be alphanumeric and length should be 
    between 5 to 20 characters

    Args:
        username (string): Username input from the user

    Returns:
        _type_: Boolean to indicate if username is in required format
    """
    return username.isalnum() and 5 <= len(username) <= 20

