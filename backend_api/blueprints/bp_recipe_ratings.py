import json
import sys
from peewee import DoesNotExist, fn
from playhouse.shortcuts import model_to_dict, dict_to_model

from flask import Blueprint, jsonify, current_app, request, g

sys.path.insert(0, '..')

from models import *
from api_exceptions import NoSuchData

bp_recipe_ratings = Blueprint(
    name='recipe_ratings',
    import_name=__name__,
    url_prefix='/recipe_ratings'
)

@bp_recipe_ratings.route('/', methods=['GET', 'POST'])
def handle_ratings():
    if request.method == 'GET':
        recipe_ratings = (
            RecipeRating
                .select()
                .order_by(fn.Random())
                .limit(10)
        )
        recipe_ratings_arr = {
            r.sk_rating: parse_ratings_json(r) for r in recipe_ratings
        }

        return json.dumps(recipe_ratings_arr), 200


    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Parser requires JSON format."}), 415
        try:
            with g.db.atomic():
                req_json = request.get_json()

                new_sk_rating = RecipeRating.insert(req_json).execute()

            fk_recipe = req_json['fk_recipe']
            return f"Rating inserted for recipe {fk_recipe}.", 201
        except DoesNotExist:
            raise NoSuchData(f'sk_recipe={fk_recipe} cannot be found in dimensions.recipe_dimension table.', status_code=404)

@bp_recipe_ratings.route('/<int:fk_recipe>', methods=['GET'])
def get_recipe_ratings(fk_recipe):
    if request.method == 'GET':
        try:
            recipe_ratings = (
                RecipeRating
                    .select()
                    .where(RecipeRating.fk_recipe == fk_recipe)
            )
            recipe_ratings_arr = {
                r.sk_rating: parse_ratings_json(r) for r in recipe_ratings
            }

            return json.dumps(recipe_ratings_arr), 200
        except DoesNotExist:
            raise NoSuchData(f'sk_recipe={fk_recipe} cannot be found in dimensions.recipe_dimension table.', status_code=404)


#
# HELPERS
#

def parse_ratings_json(r):
    return {
        "fk_recipe": r.fk_recipe.sk_recipe,
        "rating": r.rating,
        "comment": r.comment,
        "timestamp": r.timestamp.timestamp()
    }
