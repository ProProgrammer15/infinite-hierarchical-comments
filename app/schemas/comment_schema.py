from app.marshmallow import SQLAlchemyAutoSchema, validates, ValidationError
from app.models.comments import Comment


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_fk = True

    @validates("text")
    def validate_text(self, value):
        """It validates the comment text and raises validation error if it doesn't meets the criteria

        Args:
            value (_type_): Text as string

        Raises:
            ValidationError: Comment text length doesn't matches
        """
        if not 3 <= len(value) <= 200:
            raise ValidationError("Comment text must be between 3 to 200 characters.")
