from flask import Flask, jsonify, make_response, Response, request
from dotenv import load_dotenv
from werkzeug.exceptions import BadRequest, Unauthorized


from weather_app.models.favorites_model import FavoritesModel
from weather_app.models.location_model import Location
from weather_app.utils import db
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Set configuration from environment variables
app.config['ENV'] = os.getenv('FLASK_ENV')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Access API settings
API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')


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

if __name__ == '__main__':
    app.run(debug=True if app.config['ENV'] == 'development' else False)
