import json
from flask_jwt_extended import create_refresh_token

import unittest
import json
from app import create_app
from app.database import db
from app.models.users import User
from werkzeug.security import generate_password_hash


class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            hashed_password = generate_password_hash("Password@12345")
            test_user = User(username="testuser", email="test@example.com", password=hashed_password)
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup_user_success(self):
        """Test signup endpoint with valid input"""
        payload = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "Success@12345"
        }
        response = self.client.post("users/signup", json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("success", data)

    def test_signup_user_failure_existing_user(self):
        """Test signup endpoint for existing user failure"""
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password@12345"
        }
        response = self.client.post("users/signup", json=payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_login_user_success(self):
        """Test login endpoint with valid credentials"""
        payload = {
            "username": "testuser",
            "password": "Password@12345"
        }
        response = self.client.post("users/login", json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("access_token", data)
        self.assertIn("refresh_token", data)

    def test_login_user_invalid_password(self):
        """Test login endpoint with invalid password"""
        payload = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post("users/login", json=payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("errors", data)

    def test_login_user_no_user_found(self):
        """Test login endpoint for non-existent user"""
        payload = {
            "username": "nonexistent",
            "password": "password@123"
        }
        response = self.client.post("users/login", json=payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("errors", data)

    def test_refresh_token_success(self):
        """Test refresh token endpoint with valid refresh token"""
        # First, log in to get a refresh token
        login_payload = {
            "username": "testuser",
            "password": "Password@12345"
        }
        login_response = self.client.post("users/login", json=login_payload)
        refresh_token = json.loads(login_response.data)["refresh_token"]

        # Use refresh token to get a new access token
        headers = {"Authorization": f"Bearer {refresh_token}"}
        response = self.client.post("users/refresh", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("access_token", data)

