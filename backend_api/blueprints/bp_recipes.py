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
        return json.dumps(recipes_arr), 200

    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Parser requires JSON format."}), 415

        try:
            with g.db.atomic():
                req_json = request.get_json()

                for idx in range(0, len(req_json), 50):
                    rows = req_json[idx:idx + 50]
                    RecipeDimension.insert_many(rows).execute()

            total_rows = RecipeDimension.select().count()

            return f"{len(req_json)} Recipe(s) inserted. Total recipes: {total_rows}", 201
        except Exception as e:
            return e, 400


@recipes.route('/<int:sk_recipe>', methods=['GET', 'PUT', 'DELETE'])
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
        if not request.is_json:
            return jsonify({"message": "Parser requires JSON format."}), 415

        try:
            with g.db.atomic():
                req_json = request.get_json()

                (
                    RecipeDimension
                        .update(req_json)
                        .where(RecipeDimension.sk_recipe == sk_recipe)
                        .execute()
                )
                updated_recipe = (
                    RecipeDimension
                        .select()
                        .where(
                            RecipeDimension.sk_recipe == sk_recipe
                        )
                        .get()
                )
                return json.dumps(model_to_dict(updated_recipe)), 201
        except DoesNotExist:
            raise NoSuchData(f'sk_recipe={sk_recipe} cannot be found in dimensions.recipe_dimension table.', status_code=404)

    elif request.method == 'DELETE':
        try:
            with g.db.atomic():
                (
                    RecipeDimension
                        .delete()
                        .where(RecipeDimension.sk_recipe == sk_recipe)
                        .execute()
                )
            total_rows = RecipeDimension.select().count()

            return f"Recipe {sk_recipe} deleted. Total recipes: {total_rows}", 204
        except DoesNotExist:
            raise NoSuchData(f'sk_recipe={sk_recipe} cannot be found in dimensions.recipe_dimension table.', status_code=404)

def parse_recipe_json(r):
    return {
        "recipe_name": r.recipe_name,
        "recipe_subname": r.recipe_subname,
        "preparation_time": r.preparation_time,
        "fk_difficulty": r.fk_difficulty.sk_difficulty
    }