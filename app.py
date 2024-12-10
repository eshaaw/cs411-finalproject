from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from werkzeug.exceptions import BadRequest, Unauthorized
from werkzeug.security import check_password_hash
from weather_app.models.user_model import Users
from weather_app.models.favorites_model import FavoritesModel
from weather_app.models.location_model import Location
from weather_app.models.login_route import auth_bp
from weather_app.utils.sql_utils import check_database_connection
from weather_app.utils.sql_utils import get_db_connection
from weather_app.utils.db import db
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Initialize database
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    # Register Blueprints
    app.register_blueprint(auth_bp)

# Register the login blueprint
app.register_blueprint(auth_bp)

##################################################
# Healthchecks
##################################################

@app.route('/api/health', methods=['GET'])
def healthcheck():
    """
    Health check endpoint to verify the app is running.
    """
    app.logger.info("Health check")
    return make_response(jsonify({"status": "healthy"}), 200)


@app.route('/api/db-check', methods=['GET'])
def db_check():
    """
    Check if the database is reachable.
    """
    try:
        app.logger.info("Checking database connection...")
        check_database_connection()
        return make_response(jsonify({"database_status": "healthy"}), 200)
    except Exception as e:
        app.logger.error(f"Database check failed: {e}")
        return make_response(jsonify({"error": str(e)}), 500)


##################################################
# Location Management
##################################################

@app.route('/api/location', methods=['POST'])
def add_location():
    """
    Add a new location to the database.
    """
    data = request.get_json()
    city = data.get('city')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not city or latitude is None or longitude is None:
        return make_response(jsonify({"error": "City, latitude, and longitude are required"}), 400)

    try:
        location = Location.create_location(city, latitude, longitude)
        return make_response(jsonify({"status": "success", "location": location.to_dict()}), 201)
    except Exception as e:
        app.logger.error(f"Failed to add location: {e}")
        return make_response(jsonify({"error": str(e)}), 500)


@app.route('/api/location/<int:location_id>', methods=['GET'])
def get_location(location_id):
    """
    Retrieve a location by ID.
    """
    try:
        location = Location.get_location_by_id(location_id)
        return make_response(jsonify(location.to_dict()), 200)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 404)


##################################################
# Weather Endpoints
##################################################

@app.route('/api/weather/<int:location_id>', methods=['GET'])
def get_weather(location_id):
    """
    Fetch the weather for a specific location by ID.
    """
    try:
        location = Location.get_location_by_id(location_id)
        forecast = location.get_forecast()
        return make_response(jsonify({"location": location.to_dict(), "forecast": forecast}), 200)
    except Exception as e:
        app.logger.error(f"Failed to fetch weather: {e}")
        return make_response(jsonify({"error": str(e)}), 500)


##################################################
# Favorites Management
##################################################

@app.route('/api/favorites', methods=['GET', 'POST', 'DELETE'])
def manage_favorites():
    """
    Manage user's favorite locations.
    """
    user_id = request.headers.get("User-ID")
    if not user_id:
        return make_response(jsonify({"error": "User ID is required"}), 401)
    user_id = int(user_id)

    favorites = FavoritesModel(user_id)

    if request.method == 'GET':
        try:
            all_favorites = favorites.get_all_favorites()
            return make_response(jsonify([location.to_dict() for location in all_favorites]), 200)
        except ValueError as e:
            return make_response(jsonify({"error": str(e)}), 404)

    if request.method == 'POST':
        data = request.get_json()
        city = data.get('city')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if not city or latitude is None or longitude is None:
            return make_response(jsonify({"error": "City, latitude, and longitude are required"}), 400)

        try:
            location = Location(len(favorites.favorites) + 1, city, latitude, longitude)
            favorites.add_location_to_favorites(location)
            return make_response(jsonify({"status": "success", "message": "Location added to favorites"}), 201)
        except (TypeError, ValueError) as e:
            return make_response(jsonify({"error": str(e)}), 400)

    if request.method == 'DELETE':
        data = request.get_json()
        location_id = data.get('location_id')

        if location_id is None:
            return make_response(jsonify({"error": "Location ID is required"}), 400)

        try:
            favorites.remove_location_by_location_id(location_id)
            return make_response(jsonify({"status": "success", "message": "Location removed from favorites"}), 200)
        except ValueError as e:
            return make_response(jsonify({"error": str(e)}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
