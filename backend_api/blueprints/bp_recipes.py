import json
import sys
from peewee import (
    fn,
    DoesNotExist,
    IntegrityError
)

from playhouse.shortcuts import model_to_dict, dict_to_model

from flask import Blueprint, current_app, request, g

sys.path.insert(0, '..')

from models import *
from api_exceptions import NoSuchData

bp_recipes = Blueprint(
    name='recipes',
    import_name=__name__,
    url_prefix='/recipes'
)

@bp_recipes.route('/', methods=['GET', 'POST'])
def search_recipes():
    if request.method == 'GET':
        # Searching for both name and subname
        recipe_word = request.args.get('name')
        cuisine = request.args.get('cuisine')

        current_app.logger.info(f"Parameters: recipe_word={recipe_word}, cuisine={cuisine}")

        if recipe_word is not None and cuisine is not None:
            query = (
                RecipeDimension
                    .select()
                    .where(
                        (search_recipe_names(recipe_word)) &
                        (search_sk_cuisine(cuisine))
                    )
            )
        elif recipe_word is not None:
            query = (
                RecipeDimension
                    .select()
                    .where(search_recipe_names(recipe_word))
            )
        elif cuisine is not None:
            query = (
                RecipeDimension
                    .select()
                    .where(search_sk_cuisine(cuisine))
            )
        else:
            query = (
                RecipeDimension
                    .select()
                    .order_by()
                    .limit(5)
            )

        recipes_arr = {
            rep.sk_recipe: parse_recipe_json(rep) for rep in query
        }
        return json.dumps(recipes_arr), 200

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
                    RecipeDimension.insert_many(rows).execute()

            total_rows = RecipeDimension.select().count()

            return f"{len(req_json)} Recipe(s) inserted. Total recipes: {total_rows}", 201
        except IntegrityError as e:
            current_app.logger.error(sys.exc_info())
            # current_app.logger.error(dir(e))
            # current_app.logger.error(repr(e))
            return str(e), 400


@bp_recipes.route('/<int:sk_recipe>', methods=['GET', 'PUT', 'DELETE'])
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

                # Use 'returning' to avoid running another query
                query = (
                    RecipeDimension
                        .update(req_json)
                        .where(RecipeDimension.sk_recipe == sk_recipe)
                        .returning(RecipeDimension)
                )
                updated_recipes = query.execute()

                # We take first index since sk_recipe is unique.
                return json.dumps(model_to_dict(updated_recipes[0])), 201
        except DoesNotExist:
            raise NoSuchData(f'sk_recipe={sk_recipe} cannot be found in dimensions.recipe_dimension table.', status_code=404)

    # @TODO: Test this API and decide how to deal with dependencies
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


#
# HELPERS
#

def parse_recipe_json(r):
    return {
        "recipe_name": r.recipe_name,
        "recipe_subname": r.recipe_subname,
        "preparation_time": r.preparation_time,
        "fk_difficulty": r.fk_difficulty.sk_difficulty,
        "fk_cuisine": r.fk_cuisine.sk_cuisine
    }

def search_recipe_names(recipe_word):
    return (
        (fn.LOWER(RecipeDimension.recipe_name).contains(recipe_word)) |
        (fn.LOWER(RecipeDimension.recipe_subname).contains(recipe_word))
    )

def search_sk_cuisine(cuisine):
    return fn.LOWER(RecipeDimension.fk_cuisine) == fn.LOWER(cuisine)
