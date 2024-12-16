from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from flask_jwt_extended import JWTManager


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["JWT_SECRET_KEY"] = 'adffkkfkk23kdkfgkk'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

db = SQLAlchemy(app)
# jwt = JWTManager(app)

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return "<h1>Helo World</h1>"

if __name__ == "__main__":
    app.run(debug=True)
