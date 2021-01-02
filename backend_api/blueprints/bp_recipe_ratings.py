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

                batch_size = 50
                for idx in range(0, len(req_json), batch_size):
                    current_app.logger.info(f"Inserting rows {idx} to {idx + batch_size}")
                    rows = req_json[idx:idx + batch_size]
                    RecipeRating.insert_many(rows).execute()

                new_sk_rating = RecipeRating.insert(req_json).execute()

            return f"{len(req_json)} rating(s) inserted.", 201
        except Exception as e:
            current_app.logger.error(sys.exc_info())
            return str(e), 404

@bp_recipe_ratings.route('/<int:sk_rating>', methods=['GET', 'DELETE'])
def delete_recipe_ratings(sk_rating):
    if request.method == 'GET':
        try:
            with g.db.atomic():
                query = (
                    RecipeRating
                        .get_by_id(sk_rating)
                )
            return json.dumps(parse_ratings_json(query)), 201
        except DoesNotExist:
            raise NoSuchData(f'sk_rating={sk_rating} cannot be found in fact_tables.recipe_ratings table.', status_code=404)

    elif request.method == 'DELETE':
        try:
            with g.db.atomic():
                (
                    RecipeRating
                        .get_by_id(sk_rating)
                        .delete_instance()
                )
            return f"Rating deleted for sk_ratings={sk_rating}.", 201
        except DoesNotExist:
            raise NoSuchData(f'sk_rating={sk_rating} cannot be found in fact_tables.recipe_ratings table.', status_code=404)


@bp_recipe_ratings.route('/recipe/<int:fk_recipe>', methods=['GET'])
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
