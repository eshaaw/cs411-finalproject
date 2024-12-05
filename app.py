from flask import Flask
from dotenv import load_dotenv
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

@app.route('/')
def home():
    return "Flask app running!"

if __name__ == '__main__':
    app.run(debug=True if app.config['ENV'] == 'development' else False)
