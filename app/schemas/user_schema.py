from app.marshmallow import validates, ValidationError, SQLAlchemyAutoSchema, fields

from app.models.users import User
import re


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
    
    remember_me = fields.Boolean(default=False)
    
    @validates("username")
    def validates_username(self, value):
        """It validates the username field and raise validation error if it doesn't meets the criteria

        Args:
            value (_type_): Username as string

        Raises:
            ValidationError: Username length doesn't matches
            ValidationError: Username must be alphanumeric
        """
        if len(value) < 5 or len(value) > 20:
            raise ValidationError("Username must be between 5 to 20 characters.")
        if not value.isalnum():
            raise ValidationError("Username must be alphanumeric.")
        
    
    @validates("email")
    def validate_email(self, value):
        """It validates the email field and raise validation error if it doesn't meets the criteria

        Args:
            value (_type_): Email as string

        Raises:
            ValidationError: Email don't have a proper format
        """
        email_regex = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        
        if not re.match(email_regex, value):
            raise ValidationError("Invalid email format.")
    
    @validates("password")
    def validate_password(self, value):
        """It validates the password field and raise validation error if it doesn't meets the criteria

        Args:
            value (_type_): password as string

        Raises:
            ValidationError: Password length doesn't matches
            ValidationError: Password don't have any uppercase letter
            ValidationError: Password don't have any lowercase letter
            ValidationError: Password don't have any digit
            ValidationError: Password don't have any special character
        """
        if len(value) < 8 or len(value) > 20:
            raise ValidationError("Password must be between 8 and 20 characters.")
        if not re.search(r"[A-Z]", value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", value):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError("Password must contain at least one special character.")
        