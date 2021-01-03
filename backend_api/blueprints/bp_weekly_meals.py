import json
import sys

from datetime import datetime

from peewee import DoesNotExist, fn, JOIN, Table
from playhouse.shortcuts import model_to_dict, dict_to_model

from flask import Blueprint, jsonify, current_app, request, g
from flask_restful import inputs

sys.path.insert(0, '..')

from models import *
from api_exceptions import NoSuchData

bp_weekly_meals = Blueprint(
    name='weekly_meals',
    import_name=__name__,
    url_prefix='/weekly_meals'
)

@bp_weekly_meals.route('/', methods=['GET', 'POST'])
def handle_weekly_meals():
    if request.method == 'GET':
        hf_week =  request.args.get('hf_week', None)
        date = request.args.get('date', None, type=str)
        # meal_size = request.args.get('meal_size')
        default_meal = request.args.get('default_meal', None)
        default_meal = inputs.boolean(default_meal) if default_meal is not None else default_meal

        current_app.logger.info(f"Parameters: hf_week={hf_week}, date={date}, default_meal={default_meal}")

        if hf_week is None and date is None:
            hf_week = get_hf_week(get_today_sk_date())
        elif hf_week is None:
            hf_week = get_hf_week(date)

        avg_ratings = (
            RecipeRating
                .select(
                    RecipeRating.fk_recipe.alias("fk_recipe"),
                    fn.AVG(RecipeRating.rating).alias("avg_rating")
                )
                .group_by(RecipeRating.fk_recipe)
                .alias("avg_ratings")
        )

        meals_filter = (
            WeeklyMeals
                .select(
                    WeeklyMeals.fk_recipe,
                    WeeklyMeals.hellofresh_week,
                    WeeklyMeals.default_meal,
                    avg_ratings.c.avg_rating
                )
                .join(
                    avg_ratings,
                    JOIN.INNER,
                    on=(WeeklyMeals.fk_recipe == avg_ratings.c.fk_recipe),
                    attr = 'avg_ratings'
                )
                .where(filter_weekly_meals(default_meal, hf_week))
        )
        weekly_meals_arr = {
            wm.fk_recipe.sk_recipe: parse_weekly_meals(wm) for wm in meals_filter
        }

        return json.dumps(weekly_meals_arr), 200

    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Parser requires JSON format."}), 415

        req_json = request.get_json()
        hf_week = req_json['hellofresh_week']
        non_default_meals_add = req_json['non-default']['add']
        default_meals_add = req_json['default']['add']
        default_meals_rm = req_json['default']['remove']


        overlapping_fk_recipes = set(default_meals_add).intersection(set(default_meals_rm))
        if len(overlapping_fk_recipes) > 0:
            return jsonify({
                "message": f"These fk_recipe IDs: {overlapping_fk_recipes} appear in both the add and remove arrays of the JSON request. The fk_recipes specified should be unique to each array."
                }), 400

        query = (
            WeeklyMeals
                .select(
                    WeeklyMeals.hellofresh_week,
                    WeeklyMeals.fk_recipe
                    # fn.COUNT(WeeklyMeals.fk_recipe).alias('num_default_meals')
                )
                .where(
                    (WeeklyMeals.hellofresh_week == hf_week) &
                    (WeeklyMeals.default_meal == True)
                )
                .execute()
        )
        curr_default_meals_arr = []
        for row in query.execute():
            curr_default_meals_arr.append(row.fk_recipe)

        check_non_default_meals_to_remove()

        if

        """
        For the purposes of this exercise, the number of default meals
        need to be less than or equal to 3. Since the max(meal_size)=5
        for HelloFresh, I can only assume that normally the API returns
        the default meals to another algorithm that determines which recipes
        are selected for the customer based on their meal_size.

        Here we introduce a check to validate the size of the JSON arrays for default_meals_add and default_meals_rm.
        """

        max_default_meal_size = 3

        query = (
            WeeklyMeals
                .select(
                    WeeklyMeals.hellofresh_week,
                    fn.Count(WeeklyMeals.default_meal).alias('num_default_meals')
                    # fn.COUNT(WeeklyMeals.fk_recipe).alias('num_default_meals')
                )
                .where(
                    (WeeklyMeals.hellofresh_week == hf_week) &
                    (WeeklyMeals.default_meal == True)
                )
                .group_by(WeeklyMeals.hellofresh_week)
        )
        current_app.logger.info(query.sql())
        curr_def_meals = query.execute()

        for curr in curr_def_meals:
            num_default_meals = curr.num_default_meals
            break

        current_app.logger.info(f"max_default_meal_size: {max_default_meal_size}")
        current_app.logger.info(f"num_default_meals: {num_default_meals}")
        current_app.logger.info(f"len(default_meals_add): {len(default_meals_add)}")
        current_app.logger.info(f"len(default_meals_rm): {len(default_meals_rm)}")

        min_def_meal_to_rm = max(
            0,
            num_default_meals - (max_default_meal_size - len(default_meals_add))
        )
        max_def_meal_to_rm = min(
            3,
            (max_default_meal_size - num_default_meals + len(default_meals_rm))
        )

        current_app.logger.info(f"min_def_meal_to_rm: {min_def_meal_to_rm}")
        current_app.logger.info(f"max_def_meal_to_rm: {max_def_meal_to_rm}")

        if len(default_meals_add) > max_def_meal_to_rm:
            return jsonify({
                "message": f"The maximum number of default meals is {max_default_meal_size}. Since you are adding {len(default_meals_add)} default meals and there are already {num_default_meals} default meals, you must remove {min_def_meal_to_rm} default meals."
                }), 400

        if len(non_default_meals_add) > 0:
            try:
                with g.db.atomic():
                    batch_size = 50

                    for idx in range(0, len(non_default_meals), batch_size):
                        rows = [
                            build_weekly_meals_json(
                                fk_recipe,
                                hf_week,
                                is_default=False
                            ) for fk_recipe in non_default_meals[idx:idx + batch_size]
                        ]
                        query_add_non_def = (
                            WeeklyMeals
                                .insert_many(rows)
                                .on_conflict(
                                    action="ignore",
                                    conflict_target=[
                                        WeeklyMeals.fk_recipe
                                    ]
                                )
                        )
                        current_app.logger.info(query_add_non_def.sql())
                        query_add_non_def.execute()
            except Exception as e:
                current_app.logger.error(sys.exc_info())
                return f"NON_DEFAULT MEALS: {str(e)}", 404

        if len(default_meals_add) > 0:
            try:
                batch_upsert_default_meals(
                    default_meals_arr=default_meals_add,
                    hf_week=hf_week,
                    is_default=True,
                    batch_size=50
                )
            except Exception as e:
                current_app.logger.error(sys.exc_info())
                return f"DEFAULT MEALS ADD: {str(e)}", 404

        if len(default_meals_rm) > 0:
            try:
                batch_upsert_default_meals(
                    default_meals_arr=default_meals_rm,
                    hf_week=hf_week,
                    is_default=False,
                    batch_size=50
                )
            except Exception as e:
                current_app.logger.error(sys.exc_info())
                return f"DEFAULT MEALS REMOVE: {str(e)}", 404

        return "Successfully updated weekly meals", 200

@bp_weekly_meals.route('/default', methods=['GET', 'POST'])
def handle_weekly_meals():

#
# HELPERS
#

def get_today_sk_date():
    return datetime.strftime(datetime.today(), format="%Y%m%d")

def get_timestamp_from_sk_date(sk_date):
    return datetime.strptime(str(sk_date), '%Y%m%d').timestamp()

def get_hf_week(fk_date=None):
    todays_date = get_today_sk_date() if fk_date is None else fk_date

    curr_hf_week = (
        DateDimension
            .select(DateDimension.hellofresh_week)
            .where(DateDimension.sk_date == todays_date)
            .get()
    )
    return curr_hf_week.hellofresh_week

def filter_weekly_meals(default_meal, hf_week):
    if default_meal is None:
        return (WeeklyMeals.hellofresh_week == hf_week)
    else:
        return (WeeklyMeals.hellofresh_week == hf_week) & (WeeklyMeals.default_meal == default_meal)

def parse_weekly_meals(wm):
    return {
        "fk_recipe": wm.fk_recipe.sk_recipe,
        "recipe_name": wm.fk_recipe.recipe_name,
        "recipe_subname": wm.fk_recipe.recipe_subname,
        "hellofresh_week": wm.hellofresh_week,
        "default_meal": wm.default_meal,
        "avg_rating": wm.avg_ratings.avg_rating
    }

def build_weekly_meals_json(fk_recipe, hf_week, is_default):
    return {
        "fk_recipe": fk_recipe,
        "hellofresh_week": hf_week,
        "default_meal": is_default
    }

def batch_upsert_default_meals(
    default_meals_arr,
    hf_week,
    is_default,
    batch_size
):
    with g.db.atomic():
        batch_size = 50

        for idx in range(0, len(default_meals_arr), batch_size):
            rows = [
                build_weekly_meals_json(
                    fk_recipe,
                    hf_week,
                    is_default=is_default
                ) for fk_recipe in default_meals_arr[idx:idx + batch_size]
            ]
            query = (
                WeeklyMeals
                    .insert_many(rows)
                    .on_conflict(
                        action="update",
                        conflict_target=[
                            WeeklyMeals.fk_recipe,
                            WeeklyMeals.hellofresh_week
                        ],
                        update=({
                            "default_meal": is_default
                        }),
                    )
            )
            current_app.logger.info(query.sql())
            query.execute()