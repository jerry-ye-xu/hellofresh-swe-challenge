import json
import sys
from peewee import (
    fn,
    JOIN,
    SQL,
    DoesNotExist,
    IntegrityError
)

from playhouse.shortcuts import model_to_dict, dict_to_model

from flask import Blueprint, jsonify, current_app, request, g

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


# @TODO: Add information about nutritional info + instructions + ingredients
@bp_recipes.route('/<int:sk_recipe>', methods=['GET', 'PUT', 'DELETE'])
def sk_recipe_methods(sk_recipe):
    if request.method == 'GET':
        try:
            query = (
                RecipeDimension
                    .select()
                    .where(
                        RecipeDimension.sk_recipe == sk_recipe
                    )
                    .get()
            )
            return json.dumps(model_to_dict(query)), 200
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

@bp_recipes.route('/<int:sk_recipe>/instructions', methods=['GET', 'PUT'])
def sk_recipe_instructions(sk_recipe):
    if request.method == 'GET':
        if not recipe_exists(sk_recipe):
            raise NoSuchData(f'sk_recipe={sk_recipe} cannot be found in dimensions.recipe_dimension table.', status_code=404)
        # try:
        query = (
            RecipeInstruction
                .select()
                .where(
                    RecipeInstruction.fk_recipe == sk_recipe
                )
                .execute()
        )
        instructions = parse_recipe_instructions(query)

        return instructions, 200
        # except DoesNotExist:
        #     raise NoSuchData(f'sk_recipe={sk_recipe} cannot be found in dimensions.recipe_dimension table.', status_code=404)

    elif request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Parser requires JSON format."}), 415

        if not recipe_exists(sk_recipe):
            return jsonify({
                "message": f"sk_recipe={sk_recipe} cannot be found in dimensions.recipe_dimension table. You cannot create instructions for a recipe that does not exist. Please use the POST method at /recipes to create a new recipe first."
                }), 400

        table_max_step = get_max_step(sk_recipe).max_step
        req_json = request.get_json()

        if "instructions" not in req_json.keys():
            return jsonify({
                "message": "JSON requires \'instructions\' key. See example shown.",
                "instruction": {
                    "1": "instruction here",
                    "2": "another instruction",
                }
            }), 415

        is_valid, error_message = validate_instructions_json(
            req_json,
            table_max_step
        )
        if is_valid:
            exists_step_arr = []
            new_steps_arr = []
            for step, instruction in req_json['instructions'].items():
                if int(step) > table_max_step:
                    new_steps_arr.append((int(step), instruction))
                else:
                    exists_step_arr.append((int(step), instruction))

            exists_step_arr.sort()
            new_steps_arr.sort()

            current_app.logger.info(f"exists_step_arr: {exists_step_arr}")
            current_app.logger.info(f"new_steps_arr: {new_steps_arr}")

            for step, instruction in exists_step_arr:
                current_app.logger.info(f"step: {step}")
                with g.db.atomic():
                    query = (
                        RecipeInstruction
                            .update({"instruction": instruction})
                            .where(
                                (RecipeInstruction.fk_recipe.sk_recipe == sk_recipe) &
                                (RecipeInstruction.step == step)
                            )
                            .execute()
                    )

            for step, instruction in new_steps_arr:
                with g.db.atomic():
                    query = (
                        RecipeInstruction
                            .insert({
                                "fk_recipe": sk_recipe,
                                "step": step,
                                "instruction": instruction
                            })
                            .execute()
                    )

            new_max_step = get_max_step(sk_recipe).max_step
            return f"Steps {exists_step_arr} modified, steps {new_steps_arr} added for sk_recipe={sk_recipe} and new max step = {new_max_step}", 201
        else:
            return jsonify({"message": error_message}), 400

@bp_recipes.route('/<int:sk_recipe>/nutrients', methods=['GET', 'PUT'])
def sk_recipe_nutrients(sk_recipe):
    if request.method == 'GET':
        if not recipe_exists(sk_recipe):
            raise NoSuchData(f'sk_recipe={sk_recipe} cannot be found in dimensions.recipe_dimension table.', status_code=404)
        # try:
        query = (
            RecipeNutrientValue
                .select()
                .where(
                    RecipeNutrientValue.fk_recipe == sk_recipe
                )
                .execute()
        )
        nutrients = parse_recipe_nutrients(query)

        return nutrients, 200

    elif request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Parser requires JSON format."}), 415

        req_json = request.get_json()

        if "nutrients" not in req_json.keys():
            return jsonify({
                "message": "JSON requires \'nutrients\' key. See example shown.",
                "nutrients": {
                    "Carbohydrate": 0.0,
                    "Energy": 0.0,
                }
            }), 415

        for nutrient in req_json["nutrients"].keys():
            # current_app.logger.info(nutrient)
            if not nutrient_exists(nutrient):
                return jsonify({
                    "message": f"{nutrient} cannot be found in dimensions.nutrient_dimension table. Please use the PUT method at /nutrients to add the new nutrient first."
                    }), 400

        for nutrient, value in req_json["nutrients"].items():
            try:
                with g.db.atomic():
                    current_app.logger.info(f"HERE 3")

                    cte = (
                        NutrientDimension
                            .select(
                                NutrientDimension.sk_nutrient,
                                NutrientDimension.nutrient
                            )
                            .where(
                                NutrientDimension.nutrient == nutrient
                            )
                            .cte('nutrient_dimension', columns=('sk_nutrient', 'nutrient'))

                    )

                    query = (
                        RecipeNutrientValue
                            .update({
                                "value": value
                            })
                            .with_cte(cte)
                            .from_(cte)
                            .where(
                                (RecipeNutrientValue.fk_recipe == sk_recipe) &
                                (RecipeNutrientValue.fk_nutrient == SQL('nutrient_dimension.sk_nutrient'))
                            )
                    )
                    current_app.logger.error(query.sql())
                    updated_nutrients = query.execute()

            except Exception as e:
                current_app.logger.error(sys.exc_info())
                current_app.logger.error(str(e))
                return str(e), 400

        return f"Updated {list(req_json['nutrients'].keys())} for sk_recipe={sk_recipe}", 201





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

def parse_recipe_instructions(instructions):
    json_file = dict()
    json_file["instruction"] = dict()
    counter = 1
    for inst in instructions:
        if counter == 1:
            json_file["fk_recipe"] = inst.fk_recipe.sk_recipe
            json_file["recipe_name"] = inst.fk_recipe.recipe_name
            json_file["recipe_subname"] = inst.fk_recipe.recipe_subname

        json_file["instruction"][f"{counter}"] = inst.instruction

        counter += 1

    return json_file

def parse_recipe_nutrients(nutrients):
    json_file = dict()
    json_file["nutrients"] = dict()
    counter = 1
    for nts in nutrients:
        if counter == 1:
            json_file["fk_recipe"] = nts.fk_recipe.sk_recipe
            json_file["recipe_name"] = nts.fk_recipe.recipe_name
            json_file["recipe_subname"] = nts.fk_recipe.recipe_subname

        json_file["nutrients"][nts.fk_nutrient.nutrient] = nts.value

    return json_file

def search_recipe_names(recipe_word):
    return (
        (fn.LOWER(RecipeDimension.recipe_name).contains(recipe_word)) |
        (fn.LOWER(RecipeDimension.recipe_subname).contains(recipe_word))
    )

def search_sk_cuisine(cuisine):
    return fn.LOWER(RecipeDimension.fk_cuisine) == fn.LOWER(cuisine)

def recipe_exists(sk_recipe):
    does_exist = (
        RecipeDimension
            .select()
            .where(RecipeDimension.sk_recipe == sk_recipe)
            .exists()
    )
    return does_exist

def nutrient_exists(nutrient):
    does_exist = (
        NutrientDimension
            .select()
            .where(NutrientDimension.nutrient == nutrient)
            .exists()
    )
    return does_exist

def validate_instructions_json(req_json, table_max_step):
    steps_arr = []

    try:
        for step in req_json['instructions'].keys():
            if int(step) > table_max_step:
                steps_arr.append(int(step))

        if len(steps_arr) > 0:
            return check_consecutive_steps(steps_arr, table_max_step)

    except Exception as e:
        current_app.logger.error(sys.exc_info())
        return False, str(e)

    return True, None

def get_max_step(sk_recipe):
    return (
        RecipeInstruction
            .select(
                RecipeInstruction.fk_recipe,
                fn.Max(RecipeInstruction.step).alias("max_step")
            )
            .where(
                RecipeInstruction.fk_recipe == sk_recipe
            )
            .group_by(RecipeInstruction.fk_recipe)
            .get()
    )

def check_consecutive_steps(steps_arr, table_max_step):
    steps_arr = sorted(steps_arr)

    if steps_arr[0] != table_max_step + 1:
        return False, f"The step number for a single new instruction should be 1 greater than the current last step, which is {table_max_step}"

    for i in range(1, len(steps_arr)):
        if steps_arr[i] != steps_arr[i-1] + 1:
            return False, "When adding multiple instructions, step numbers should increment by one."

    return True, None