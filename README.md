# cs411-finalproject
Features
1. User Management
Create User: Register a new user with a username and password.
Delete User: Remove a user from the database by username.
Login: Authenticate a user using their username and password.
2. Weather API
Fetch weather data (currently placeholder functionality, can be extended to include real weather APIs).
3. Health Check
Verify the application's health and server status.
4. Database Management
Initialize the database by creating or recreating all tables.
Endpoints
Health Check
GET /api/health:
Response: {"status": "healthy"}
User Management
POST /api/create-user:

Request: {"username": "your_username", "password": "your_password"}
Response: {"status": "user added", "username": "your_username"}
DELETE /api/delete-user:

Request: {"username": "your_username"}
Response: {"status": "user deleted", "username": "your_username"}
POST /api/login:

Request: {"username": "your_username", "password": "your_password"}
Response: {"message": "Login successful"}
Database Management
POST /api/init-db:
Response: {"status": "success", "message": "Database initialized successfully."}
Weather API
GET /api/weather:
Response: {"status": "success", "weather": "Sunny, 25°C"}
Installation
Prerequisites
Python 3.8+
pip (Python package manager)
SQLite (pre-installed in Python)
Steps
Clone the repository:

bash
Copy code
git clone https://github.com/eshaaw/cs411-finalproject.git
cd weather-app
Create a virtual environment and activate it:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the root directory with the following content:
makefile
Copy code
FLASK_APP=app.py
FLASK_ENV=development
Initialize the database:

bash
Copy code
flask run --host=0.0.0.0 --port=5000
Use the /api/init-db endpoint to initialize the database tables.
Run the application:

bash
Copy code
flask run
Access the app at: http://localhost:5000

Testing
Run Unit Tests
To run the unit tests, execute:

bash
Copy code
pytest
Project Structure
bash
Copy code
weather-app/
│
├── weather_app/                  # Application code
│   ├── models/                   # Database models
│   │   ├── user_model.py
│   │   ├── login_route.py
│   │
│   ├── utils/                    # Utility modules
│   │   ├── db.py                 # Database connection
│   │   ├── sql_utils.py          # SQL utility functions
│   │
│   ├── __init__.py               # Initialize Flask app
│   └── app.py                    # Main application entry point
│
├── tests/                        # Unit tests
│   ├── test_login_route.py
│   ├── test_user_model.py
│
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation
Contributing
Fork the repository.
Create a new branch for your feature:
bash
Copy code
git checkout -b feature-name
Commit your changes and push to the branch:
bash
Copy code
git push origin feature-name
Open a pull request.
