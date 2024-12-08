from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from werkzeug.exceptions import BadRequest, Unauthorized
from werkzeug.security import check_password_hash
from weather_app.models.user_model import Users
from weather_app.utils.sql_utils import get_db_connection
from weather_app.utils.db import db
from weather_app.models.login_route import auth_bp

# Load environment variables from .env file
load_dotenv()


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

    ####################################################
    #
    # Healthcheck
    #
    ####################################################

    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        """
        Health check route to verify the service is running.

        Returns:
            JSON response indicating the health status of the service.
        """
        app.logger.info('Health check')
        return make_response(jsonify({'status': 'healthy'}), 200)

    ####################################################
    #
    # User Management
    #
    ####################################################

    @app.route('/api/create-user', methods=['POST'])
    def create_user() -> Response:
        """
        Route to create a new user.

        Expected JSON Input:
            - username (str): The username for the new user.
            - password (str): The password for the new user.

        Returns:
            JSON response indicating the success of user creation.
        """
        app.logger.info('Creating a new user')
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                raise BadRequest("Invalid input. Both username and password are required.")

            Users.create_user(username, password)
            app.logger.info("User added successfully: %s", username)
            return make_response(jsonify({'status': 'user added', 'username': username}), 201)

        except Exception as e:
            app.logger.error("Failed to add user: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/delete-user', methods=['DELETE'])
    def delete_user() -> Response:
        """
        Route to delete a user.

        Expected JSON Input:
            - username (str): The username of the user to be deleted.

        Returns:
            JSON response indicating the success of user deletion.
        """
        app.logger.info('Deleting user')
        try:
            data = request.get_json()
            username = data.get('username')

            if not username:
                raise BadRequest("Invalid input. Username is required.")

            Users.delete_user(username)
            app.logger.info("User deleted successfully: %s", username)
            return make_response(jsonify({'status': 'user deleted', 'username': username}), 200)

        except Exception as e:
            app.logger.error("Failed to delete user: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/login', methods=['POST'])
    def login() -> Response:
        """
        Route to authenticate a user.

        Expected JSON Input:
            - username (str): The username of the user.
            - password (str): The password of the user.

        Returns:
            JSON response indicating the success or failure of authentication.
        """
        app.logger.info('User login attempt')
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                raise BadRequest("Invalid input. Username and password are required.")

            with get_db_connection() as conn:
                user = Users.query.filter_by(username=username).first()
                if not user or not check_password_hash(user.password, password):
                    raise Unauthorized("Invalid username or password.")

            app.logger.info("User logged in successfully: %s", username)
            return jsonify({'message': 'Login successful'}), 200

        except Unauthorized as e:
            app.logger.warning(str(e))
            return jsonify({'error': str(e)}), 401

        except Exception as e:
            app.logger.error("Login failed: %s", str(e))
            return jsonify({'error': "An unexpected error occurred."}), 500

    ####################################################
    #
    # Database Management
    #
    ####################################################

    @app.route('/api/init-db', methods=['POST'])
    def init_db():
        """
        Route to initialize the database.

        Returns:
            JSON response indicating the success of the operation.
        """
        try:
            with app.app_context():
                app.logger.info("Initializing database.")
                db.drop_all()
                db.create_all()
            return jsonify({"status": "success", "message": "Database initialized successfully."}), 200

        except Exception as e:
            app.logger.error("Failed to initialize database: %s", str(e))
            return jsonify({"status": "error", "message": "Failed to initialize database."}), 500

    ####################################################
    #
    # Weather Endpoints (Placeholder)
    #
    ####################################################

    @app.route('/api/weather', methods=['GET'])
    def get_weather():
        """
        Placeholder route for fetching weather data.

        Returns:
            JSON response with mock weather data.
        """
        app.logger.info("Fetching weather data.")
        return jsonify({"status": "success", "weather": "Sunny, 25°C"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
