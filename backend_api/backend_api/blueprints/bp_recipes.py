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

from backend_api.models import *
from backend_api.api_exceptions import NoSuchData

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

        req_json = request.get_json()

        if not check_valid_recipe_post_keys(list(req_json.keys())):
            return jsonify({"message": "JSON must contain ['recipe', 'ingredients', 'instructions', 'nutrients']"}), 400

        for nutrient in req_json['nutrients']:
            if not nutrient_exists(nutrient):
                return jsonify({"message": "Nutrients in JSON must already be in nutrient_dimension"}), 400

        nutrients_to_insert = req_json['nutrients']
        instructions_to_insert = req_json['ingredients']

        try:
            with g.db.atomic():
                new_sk_recipe = (
                    RecipeDimension
                        .insert(req_json['recipe'])
                        .execute()
                )

                _ = (
                    RecipeIngredient
                        .insert_many(
                            prepare_ingredients_insertion(req_json['ingredients'], new_sk_recipe)
                        )
                        .on_conflict(
                            action='ignore'
                        )
                )

                _ = (
                    RecipeInstruction
                        .insert_many(
                            prepare_instructions_insertion(req_json['instructions'], new_sk_recipe)
                        )
                        .on_conflict(
                            action='ignore'
                        )
                )

                _ = (
                    RecipeNutrientValue
                        .insert_many(
                            prepare_nutrients_insertion(req_json['nutrients'], new_sk_recipe)
                        )
                        .on_conflict(
                            action='ignore'
                        )
                )

            return jsonify({"message": f"Added new recipe. sk_recipe={new_sk_recipe}."}), 201
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

    elif request.method == 'DELETE':
        try:
            with g.db.atomic():
                (
                    RecipeNutrientValue
                        .delete()
                        .where(RecipeNutrientValue.fk_recipe == sk_recipe)
                        .execute()
                )

                (
                    RecipeIngredient
                        .delete()
                        .where(RecipeIngredient.fk_recipe == sk_recipe)
                        .execute()
                )

                (
                    RecipeInstruction
                        .delete()
                        .where(RecipeInstruction.fk_recipe == sk_recipe)
                        .execute()
                )
                (
                    RecipeRating
                        .delete()
                        .where(RecipeRating.fk_recipe == sk_recipe)
                        .execute()
                )
                (
                    WeeklyMeals
                        .delete()
                        .where(WeeklyMeals.fk_recipe == sk_recipe)
                        .execute()
                )
                (
                    RecipeDimension
                        .delete()
                        .where(RecipeDimension.sk_recipe == sk_recipe)
                        .execute()
                )
            # total_rows = RecipeDimension.select().count()

        except DoesNotExist:
            raise NoSuchData(f'sk_recipe={sk_recipe} cannot be found in dimensions.recipe_dimension table.', status_code=404)

        current_app.logger.info("REACH HERE???")

        return jsonify({"message": f"Recipe={sk_recipe} deleted."}), 204

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
                                (RecipeInstruction.fk_recipe == sk_recipe) &
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
            return jsonify({"message": f"Steps {exists_step_arr} modified, steps {new_steps_arr} added for sk_recipe={sk_recipe} and new_max_step={new_max_step}."}), 201
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
                    # current_app.logger.info(f"HERE 3")

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

        return jsonify({"message": f"Updated {list(req_json['nutrients'].keys())} for sk_recipe={sk_recipe}"}), 201

@bp_recipes.route('/<int:sk_recipe>/ingredients', methods=['GET', 'PUT'])
def sk_recipe_ingredients(sk_recipe):
    if request.method == 'GET':
        if not recipe_exists(sk_recipe):
            raise NoSuchData(f'sk_recipe={sk_recipe} cannot be found in dimensions.recipe_dimension table.', status_code=404)
        # try:
        query = (
            RecipeIngredient
                .select()
                .where(
                    RecipeIngredient.fk_recipe == sk_recipe
                )
                .execute()
        )
        ingredients = parse_recipe_ingredients(query)

        return ingredients, 200

    elif request.method == 'PUT':
        if not request.is_json:
            return jsonify({"message": "Parser requires JSON format."}), 415

        req_json = request.get_json()

        if "ingredients" not in req_json.keys():
            return jsonify({
                "message": "JSON requires \'ingredients\' key. See example shown.",
                "ingredients": {
                    "name": "bread",
                    "serving_size": 2,
                    "value": 1,
                    "unit": "loaf"
                }
            }), 415

        for ingredient in req_json["ingredients"].keys():
            if not ingredient_exists(ingredient):
                return jsonify({
                    "message": f"{ingredient} cannot be found in dimensions.nutrient_dimension table. Please use the PUT method at /nutrients to add the new nutrient first."
                    }), 400

        for ingredient, ing_json in req_json["ingredients"].items():
            try:
                with g.db.atomic():

                    cte = (
                        IngredientDimension
                            .select(
                                IngredientDimension.sk_ingredient,
                                IngredientDimension.ingredient
                            )
                            .where(
                                IngredientDimension.ingredient == ingredient
                            )
                            .cte('ingredient_dimension', columns=('sk_ingredient', 'ingredient'))

                    )
                    ing_dim = (
                        IngredientDimension
                            .select()
                            .where(
                                IngredientDimension.ingredient == ingredient
                            )
                            .get()
                    )

                    current_app.logger.info("IngredientDimension")
                    current_app.logger.info(f"ing_dim.sk_ingredient: {ing_dim.sk_ingredient}")

                    rp_ing = (
                        RecipeIngredient
                            .select()
                            .where(
                                (RecipeIngredient.fk_recipe == sk_recipe) &
                                (RecipeIngredient.fk_ingredient == ing_dim.sk_ingredient)
                            )
                            .execute()
                    )
                    current_app.logger.info("RecipeIngredient")
                    current_app.logger.info(f"len(rp_ing): {len(rp_ing)}")

                    # Default values, which can be overwritten
                    default_values = {
                        "fk_recipe": sk_recipe,
                        "fk_ingredient": ing_dim.sk_ingredient,
                        "serving_size": 2,
                        "value": 0,
                        "unit": "",
                    }

                    if len(rp_ing) > 0:
                        for rp in rp_ing:
                            serving_size = rp.serving_size
                            value = rp.value
                            unit = rp.unit

                        rp_ing_values = {
                            "fk_recipe": sk_recipe,
                            "fk_ingredient": ing_dim.sk_ingredient,
                            "serving_size": serving_size,
                            "value": value,
                            "unit": unit,
                        }
                        default_values.update(rp_ing_values)

                    current_app.logger.info(default_values)

                    # We update the default values to ensure
                    # INSERT doesn't run into null constraint
                    # issues.
                    default_values.update(ing_json)
                    current_app.logger.info(default_values)

                    query = (
                        RecipeIngredient
                            .insert(default_values)
                            .on_conflict(
                                action="update",
                                conflict_target=[
                                    RecipeIngredient.fk_ingredient,
                                    RecipeIngredient.fk_recipe
                                ],
                                update=(ing_json),
                                where=(RecipeIngredient.fk_recipe == sk_recipe)
                            )
                    )
                    current_app.logger.error(query.sql())
                    updated_ingredients = query.execute()

            except Exception as e:
                current_app.logger.error(sys.exc_info())
                return str(e), 400

        return jsonify({"message": f"Updated {list(req_json['ingredients'].keys())} for sk_recipe={sk_recipe}"}), 201


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

def parse_recipe_ingredients(ingredients):
    json_file = dict()
    json_file["ingredients"] = []
    counter = 1
    for ing in ingredients:
        if counter == 1:
            json_file["fk_recipe"] = ing.fk_recipe.sk_recipe
            json_file["recipe_name"] = ing.fk_recipe.recipe_name
            json_file["recipe_subname"] = ing.fk_recipe.recipe_subname

        json_file["ingredients"].append({
            "sk_ingredient": ing.fk_ingredient.sk_ingredient,
            "name": ing.fk_ingredient.ingredient,
            "serving_size": ing.serving_size,
            "value": ing.value,
            "unit": ing.unit
        })

    return json_file

def check_valid_recipe_post_keys(keys_arr):
    keys_set = set(['recipe', 'ingredients', 'nutrients', 'instructions'])
    return keys_set == set(keys_arr)

# def prepare_ingredients_insertion(json, fk_recipe):
#     will_deliver = [
#         {
#             "ingredient": j['ingredient'],
#             "included_in_delivery": True
#         }
#         for j in json['will_deliver']
#     ]
#     will_not_deliver = [
#         {
#             "ingredient": j['ingredient'],
#             "included_in_delivery": False
#         }
#         for j in json['will_not_deliver']
#     ]

#     return will_deliver + will_not_deliver

def prepare_ingredients_insertion(arr, fk_recipe):
    return [
        {**json, **{"fk_recipe": fk_recipe}} for json in arr
    ]

def prepare_instructions_insertion(json, fk_recipe):

    return [
        {
            "fk_recipe": fk_recipe,
            k: v
        }
        for k, v in json.items()
    ]

def prepare_nutrients_insertion(json, fk_recipe):

    return [
        {
            "fk_recipe": fk_recipe,
            k: v
        }
        for k, v in json.items()
    ]

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

def ingredient_exists(ingredient):
    """
    We can also prefetch all the ingredients. However, if the number of ingredients is significantly large, it will affect performance.

    Perhaps .exists() function has an optimised implementation under the hood, or we can use the in_() function.

    For the sake of this exercise we keep it simple.
    """
    does_exist = (
        IngredientDimension
            .select()
            .where(IngredientDimension.ingredient == ingredient)
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
        return False, f"The step number for a single new instruction should be 1 greater than the current last step, which is {table_max_step}."

    for i in range(1, len(steps_arr)):
        if steps_arr[i] != steps_arr[i-1] + 1:
            return False, "When adding multiple instructions, step numbers should increment by one."

    return True, None