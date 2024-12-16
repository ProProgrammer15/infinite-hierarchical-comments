import json

from flask import request, jsonify

from app.comments import bp
from app.extensions import db
from app.models.users import User
from app.models.comments import Comment
from app.utils.comment_utils import comment_text_length_validation
from app.utils.comment_utils import get_comments_tree


@bp.route('/create', methods=["POST"])
def create_comment():
    """It validates the comment text and user_id and creates a new comment

    Returns:
        _type_: Success or failure message as json
    """
    request_data = json.loads(request.data)
    
    text = request_data.get("text", None)
    user_id = request_data.get("user_id", None)
    parent_id = request_data.get("parent_id", None)
    
    if text is None:
        return jsonify({"error": "text field is required"}), 400
    
    if not comment_text_length_validation(text):
        return jsonify({"error": "Text must be between 3 and 200 characters"})
    
    if user_id is None:
        return jsonify({"error": "user_id field is required"}), 400
    
    user = db.session.query(User).filter_by(id=user_id).first()
    parent_comment = db.session.query(Comment).filter_by(id=parent_id).first()

    if user is None:
        return jsonify({"error": "User doesn't exists"}), 400
    
    if parent_comment:
        comment = Comment(text=text, user=user, parent_id=parent_comment.id)
    else:
        comment = Comment(text=text, user=user)
        
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({"success": "Comment created successfully"})


@bp.route('/list')
def get_comments():
    """It returns all the comments in a tree based heirarchy level

    Returns:
        _type_: Comments list as json
    """
    comments = get_comments_tree()
    
    return jsonify({"comments": comments}), 200
