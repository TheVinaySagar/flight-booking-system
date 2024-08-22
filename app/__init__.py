from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create instances of Flask, SQLAlchemy, and LoginManager
app = Flask(__name__)
app.config.from_object('config.Config')  # Load configuration from config.py

# Initialize SQLAlchemy with the app
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # View to redirect to when a login is required

# Import the User model to be used by Flask-Login
from app.models import User

# Set up the user loader callback function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes after initializing app and db to avoid circular imports
from app import routes
