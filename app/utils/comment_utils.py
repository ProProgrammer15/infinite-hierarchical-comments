from sqlalchemy.orm import selectinload
from app.models.comments import Comment


def build_tree(comment):
    """It takes the comment object and recursively calls the following function if 
    there are replies for any comment
    Args:
        comment (object): Comment object

    Returns:
        _type_: Constructed json for each comment
    """
    return {
        "id": comment.id,
        "user_id": comment.user_id,
        "username": comment.user.username,
        "text": comment.text,
        "created_at": comment.posted_at,
        # recursively calls the function if there are any replies
        "replies": [build_tree(reply) for reply in comment.replies],
    }


def get_comments_tree():
    """It constructs a query to fetch the top level of comments that have
    no parent comment and constructs json object for each comment

    Returns:
        _type_: Comment objects as list
    """
    
    # Fetch root comments that have no parent comment, ordered by created_at
    root_comments = (
        Comment.query.filter_by(parent_id=None)
        .order_by(Comment.posted_at)
        .options(
            selectinload(Comment.replies),  # Preload replies
            selectinload(Comment.user)  # Preload user 
            )
        .all()
    )

    return [build_tree(comment) for comment in root_comments]
