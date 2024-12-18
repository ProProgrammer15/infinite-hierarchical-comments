import unittest
import json
from app import create_app
from app.database import db
from app.models.users import User
from app.models.comments import Comment
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

class TestCommentsRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and database."""
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            hashed_password = generate_password_hash("Password@123")
            self.user = User(username="testuser", email="test@example.com", password=hashed_password)
            db.session.add(self.user)
            db.session.commit()

            self.access_token = create_access_token(identity=self.user.id)

    def tearDown(self):
        """Tear down the database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_comment_success(self):
        """Test creating a comment successfully."""
        payload = {
            "text": "This is a test comment",
            "user_id": self.user.id
        }
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = self.client.post("comments/create", json=payload, headers=headers)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("success", data)
        self.assertEqual(data["success"], "Comment created successfully")

    def test_create_comment_user_not_found(self):
        """Test creating a comment with an invalid user ID."""
        payload = {
            "text": "Invalid user comment",
            "user_id": 999
        }
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = self.client.post("comments/create", json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "User doesn't exist")

    def test_create_comment_not_current_user(self):
        """Test creating a comment with mismatched user ID."""
        payload = {
            "text": "User ID mismatch",
            "user_id": self.user.id + 1
        }
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = self.client.post("comments/create", json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "User doesn't exist")

    def test_get_comments_success(self):
        """Test retrieving the list of comments."""
        comment = Comment(text="Test comment", user_id=self.user.id)
        with self.app.app_context():
            db.session.add(comment)
            db.session.commit()

        response = self.client.get("comments/list")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("comments", data)
        self.assertEqual(len(data["comments"]), 1)

    def test_delete_comment_success(self):
        """Test deleting a comment successfully."""
        comment = Comment(text="Comment to delete", user_id=self.user.id)
        with self.app.app_context():
            db.session.add(comment)
            db.session.commit()
            comment_id = comment.id

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = self.client.delete(f"comments/delete/{comment_id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("success", data)
        self.assertEqual(data["success"], "Comment deleted successfully")

        with self.app.app_context():
            deleted_comment = db.session.query(Comment).filter_by(id=comment.id).first()
            self.assertIsNone(deleted_comment)

    def test_delete_comment_not_found(self):
        """Test deleting a non-existent comment."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = self.client.delete("comments/delete/999", headers=headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Comment does not exist")

    def test_delete_comment_unauthorized_user(self):
        """Test deleting a comment that doesn't belong to the current user."""
        other_user = User(username="otheruser", email="other@example.com", password="password456")
        with self.app.app_context():
            db.session.add(other_user)
            db.session.commit()

            comment = Comment(text="Other user's comment", user_id=other_user.id)
            db.session.add(comment)
            db.session.commit()
            comment_id = comment.id
            
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = self.client.delete(f"comments/delete/{comment_id}", headers=headers)
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "You are not authorized to delete this comment")
