from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database import db
from app.marshmallow import ValidationError
from app.models.users import User
from app.models.comments import Comment
from app.utils.comment_utils import get_comments_tree
from app.schemas.comment_schema import CommentSchema

comments_blueprint = Blueprint("comments", __name__)
comment_schema = CommentSchema()


@comments_blueprint.route('/create', methods=["POST"])
@jwt_required()
def create_comment():
    """It validates the comment text and user_id and creates a new comment

    Returns:
        _type_: Success or failure message as json
    """
    try:
        # Deserialize and validate the request input
        request_data = comment_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    text = request_data["text"]
    user_id = request_data["user_id"]
    parent_id = request_data.get("parent_id")

    current_user_id = get_jwt_identity()
    user = db.session.query(User).filter_by(id=user_id).first()
    parent_comment = None
    
    if not user:
        return jsonify({"error": "User doesn't exist"}), 400

    if not user_id == current_user_id:
        return jsonify({"error": "User id doesn't belongs to current user"}), 400
    
    if parent_id:
        parent_comment = db.session.query(Comment).filter_by(id=parent_id).first()
        
        if not parent_comment:
            return jsonify({"error": "Parent comment doesn't exist"}), 400

    if parent_comment:
        comment = Comment(text=text, user=user, parent_id=parent_comment.id)
    else:
        comment = Comment(text=text, user=user)

    db.session.add(comment)
    db.session.commit()

    return jsonify({"success": "Comment created successfully"}), 201


@comments_blueprint.route('/list')
def get_comments():
    """It returns all the comments in a tree based heirarchy level

    Returns:
        _type_: Comments list as json
    """
    comments = get_comments_tree()
    
    return jsonify({"comments": comments}), 200


@comments_blueprint.route('/delete/<int:pk>', methods=["DELETE"])
@jwt_required()
def delete_comment(pk):
    """
    Deletes a comment after validating that it belongs to the current user.

    Args:
        pk (int): Primary key of the comment to delete.

    Returns:
        JSON response indicating success or failure.
    """
    current_user_id = get_jwt_identity()
    comment = db.session.query(Comment).filter_by(id=pk).first()

    if not comment:
        return jsonify({"error": "Comment does not exist"}), 404

    if comment.user_id != current_user_id:
        return jsonify({"error": "You are not authorized to delete this comment"}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"success": "Comment deleted successfully"}), 200
