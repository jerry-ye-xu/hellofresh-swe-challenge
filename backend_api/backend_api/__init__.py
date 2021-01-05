import os

from flask import Flask, g, jsonify

from backend_api.api_exceptions import NoSuchData
from backend_api.models import psql_db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # Load the default configuration

    app.logger.info(f"{__name__}")
    app.logger.info(f"{app.instance_path}")

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

    from .blueprints import (
        bp_recipes,
        bp_nutrients,
        bp_ingredients,
        bp_cuisines,
        bp_recipe_ratings,
        bp_weekly_meals
    )

    app.register_blueprint(bp_recipes.bp_recipes)
    app.logger.info(f"Recipes blueprint imported.")

    app.register_blueprint(bp_nutrients.bp_nutrients)
    app.logger.info(f"Nutrients blueprint imported.")

    app.register_blueprint(bp_ingredients.bp_ingredients)
    app.logger.info(f"Ingredients blueprint imported.")

    app.register_blueprint(bp_cuisines.bp_cuisines)
    app.logger.info(f"Cuisines blueprint imported.")

    app.register_blueprint(bp_recipe_ratings.bp_recipe_ratings)
    app.logger.info(f"Recipe ratings blueprint imported.")

    app.register_blueprint(bp_weekly_meals.bp_weekly_meals)
    app.logger.info(f"Weekly meals blueprint imported.")

    @app.before_request
    def before_request():
        g.db = psql_db
        g.db.connect()

    @app.after_request
    def after_request(response):
        g.db.close()
        return response

    @app.route('/')
    def hello():
        return 'Welcome to the HelloFresh SWE Challenge Backend API.', 200

    @app.errorhandler(NoSuchData)
    def handle_no_such_data_error(error):
        res = jsonify(error.to_dict())
        res.status_code = error.status_code

        return res

    app.logger.info(f"Application factory is complete for: {app}")
    return app