from flask_marshmallow import Marshmallow

marshmallow = Marshmallow()

from marshmallow import validates, ValidationError, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
