from flask import Flask
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Register Blueprints here
    from .routes import route_bp
    app.register_blueprint(route_bp)

    CORS(app)
    return app
