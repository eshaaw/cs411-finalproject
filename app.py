<<<<<<< HEAD
from flask import Flask, jsonify, make_response, Response, request
from dotenv import load_dotenv
from werkzeug.exceptions import BadRequest, Unauthorized


from weather_app.models.favorites_model import FavoritesModel
from weather_app.models.location_model import Location
from weather_app.utils import db
import os

# Load environment variables from .env
load_dotenv()
=======
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
>>>>>>> 6675d19 (added the user_model)

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

<<<<<<< HEAD

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Recreate all tables

    favorites_model = FavoritesModel()

    ####################################################
    #
    # Healthchecks
    #
    ####################################################

@app.route('/')
def home():
    return "Flask app running!"
=======
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

# Create tables in the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
>>>>>>> 6675d19 (added the user_model)

if __name__ == '__main__':
    app.run(debug=True)
