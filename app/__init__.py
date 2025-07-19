from flask import Flask
from app.routes.main import main_blueprint
from app.routes.api import api
from app.routes.file_upload import file_upload
from app.routes.text_upload import text_upload
from app.extensions import db, socketio
from app.models.models import TextContent, FileReference

def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

   #config for file upload
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # max 16 megabytes
    app.config['UPLOAD_FOLDER'] = 'file_upload'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'svg'}

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins='*')

    # Create tables
    with app.app_context():
        db.create_all()

    # Register Blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(file_upload)
    app.register_blueprint(text_upload, url_prefix='/text')

    return app