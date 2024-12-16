from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class User(db.Model):
    """It generates a User model with fields id, username, email and password

    Args:
        db (_type_): Database object

    Returns:
        _type_: Formatted string of id and username as instance representation
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    
    def __repr__(self):
        return f"{self.id} {self.username}"
    