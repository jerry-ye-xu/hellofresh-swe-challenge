import json
import sys
from peewee import DoesNotExist
from playhouse.shortcuts import model_to_dict, dict_to_model

from flask import Blueprint, current_app, request, g

sys.path.insert(0, '..')

from models import *
from api_exceptions import NoSuchData

recipes = Blueprint(
    name='recipes',
    import_name=__name__,
    url_prefix='/recipes'
)

@recipes.route('/', methods=['GET', 'POST'])
def handle_recipes():
    if request.method == 'GET':
        recipes = RecipeDimension.select()
        recipes_arr = {
            r.sk_recipe: parse_recipe_json(r) for r in recipes
        }
        print(f"recipes_arr: {recipes_arr}")
        return json.dumps(recipes_arr), 200

    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 415

        req_json = request.get_json()

        # cur = g.db.cursor()
        # max_sk = g.db.last_insert_id(cur)
        # max_sk
        # current_app.logger.info(f"max_sk: {max_sk}")

        with g.db.atomic():
            RecipeDimension.create(
                recipe_name=req_json['recipe_name'],
                recipe_subname=req_json['recipe_subname'],
                preparation_time=req_json['preparation_time'],
                fk_difficulty=req_json['fk_difficulty']
            )
            # new_recipe.save(force_insert=True)
        # new_recipe.save(force_insert=True)

        return request.get_json(), 201


@recipes.route('/<int:sk_recipe>', methods=['GET', 'PUT'])
def sk_recipe_methods(sk_recipe):
    if request.method == 'GET':
        try:
            recipe = (
                RecipeDimension
                    .select()
                    .where(
                        RecipeDimension.sk_recipe == sk_recipe
                    )
                    .get()
            )
            return json.dumps(model_to_dict(recipe)), 200
        except DoesNotExist:
            raise NoSuchData(f'sk_recipe={sk_recipe} cannot be found in dimensions.recipe_dimension table.', status_code=404)

    elif request.method == 'PUT':
        return 'ERROR: Method has not been implemented yet.', 404

def parse_recipe_json(r):
    current_app.logger.info(f"r: {r}")
    current_app.logger.info(f"r.fk_difficulty: {r.fk_difficulty}")
    return {
        "recipe_name": r.recipe_name,
        "recipe_subname": r.recipe_subname,
        "preparation_time": r.preparation_time,
        "fk_difficulty": r.fk_difficulty.sk_difficulty
    }