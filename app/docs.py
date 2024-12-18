import json

from flask import Blueprint
from flasgger import Swagger


docs_bp = Blueprint("/docs", __name__)

def initialize_swagger(app):
    """
    Function to initialize Swagger documentation with the app instance.
    This function uses Flasgger's Swagger class.
    """
    with open("schema.json", "r+") as f:
        schemas = json.load(f)
        
        Swagger(app, template=schemas)
