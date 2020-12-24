import os

from flask import Flask
from models import psql_db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Load the default configuration
    app.config.from_pyfile('config.py', silent=False)

    # Load environment specific configuration files
    # inside the instance folder
    if test_config is None:
        # No such file exists yet, so silently fail.
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.logger.info(f"app.debug={app.debug}")
    app.logger.info(f"app.secret_key={app.secret_key}")

    try:
        os.makedirs(app.instance_path)
    except OSError as e:
        app.logger.info(e)


    from . import db
    db.init_app(app)
    app.logger.info(f"PostgreSQL Database initialised.")

    from .blueprints import bp_recipes, bp_ratings
    app.register_blueprint(bp_recipes.recipes)
    app.logger.info(f"Recipes blueprint imported.")

    app.register_blueprint(bp_ratings.ratings)
    app.logger.info(f"Ratings blueprint imported.")

    @app.before_request
    def before_request():
        g.db.connect()

    @app.after_request
    def after_request(response):
        g.db.close()
        return response

    @app.route('/')
    def hello():
        return 'Hello World!'

    app.logger.info(f"Application factory is complete for: {app}")
    return app