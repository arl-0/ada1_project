from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Start database and login manager 
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuration settings

    app.config['SECRET_KEY'] = 'make_more_secure_later'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ada1.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG_BYPASS_STARTUP'] = False  # Toggle this for development


    # Initialize extension within app
    db.init_app(app)
    login_manager.init_app(app)

    # Set login page used by @login_required
    login_manager.login_view = 'main.login'

    #Import and register blueprint (routes)
    from .routes import main
    app.register_blueprint(main)

    return app