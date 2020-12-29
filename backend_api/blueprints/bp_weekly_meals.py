import json
import sys

from datetime import datetime

from peewee import DoesNotExist, fn, JOIN, Table
from playhouse.shortcuts import model_to_dict, dict_to_model

from flask import Blueprint, current_app, request, g
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