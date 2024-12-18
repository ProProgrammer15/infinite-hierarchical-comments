from datetime import datetime, timezone
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import db


class Comment(db.Model):
    """It creates a Comment table with fields id, text, posted_at, user_id as foreign key of User 
    and parent_id as foriegn key of Comment model to represent the parent of each comment instance

    Args:
        db (_type_): Database object
    
    Returns:
        _type_: Formatted string of id and text as instance representation
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    posted_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user = db.relationship("User", backref="comments", foreign_keys=[user_id])

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("comment.id"), nullable=True)
    parent = db.relationship("Comment", remote_side=[id], backref="replies")
    
    def __repr__(self):
        return f"{self.id} {self.text}"
    