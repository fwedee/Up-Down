from flask import Flask
from app.routes.main import main_blueprint
from app.routes.api import api
from app.extensions import db

def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api, url_prefix='/api')

    return app