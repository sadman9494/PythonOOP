from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from app.config import Config

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    jwt.init_app(app)

    from app.routes import auth_bp, api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    return app
