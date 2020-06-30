"""The application factory of the backend."""
import os
from pathlib import Path
from flask import Flask
from flask_cors import CORS

from backend.database import db
from backend.resources import BLUEPRINTS


def create_app(test_config=None):
    """
    Creates the application and register all resources to it.

    :param test_config: optional config for Flask for testing purposes, default is None
    :return: Created application
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(24),
        DATABASE=os.path.join(app.instance_path, 'backend.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.root_path, '../files'),
        MAX_CONTETN_LENGTH=5 * 1024 * 1024,
        ALLOWED_EXTENSIONS={'png', 'jpeg', 'jpg', 'gif', 'bmp'}
    )
    CORS(app)
    # ToDo: for production add real cors-options

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)  # load the instance config if exists
    else:
        app.config.from_mapping(test_config)  # load test config

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)

    return app
