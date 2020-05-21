## @package backend.util.__init__
#  The application factory of the backend
import os
from flask import Flask, abort

## Creates the application and register all resources to it.
#  @param test_config the configuration for testing purposes, default is None
#  @return the created application
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'backend.sqlite'),
    )
    if test_config is None:
        #load the instance config if exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load test config
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from backend.util import db
    db.init_app(app)

    #add new resources in this block
    from .resources import ( 
        sample,
        institutions,
        projects,
    )
    app.register_blueprint(sample.bp)
    app.register_blueprint(institutions.bp)
    app.register_blueprint(projects.bp)

    return app
