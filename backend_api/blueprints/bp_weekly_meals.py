import json
import sys

from datetime import datetime

from peewee import DoesNotExist, fn, JOIN
from playhouse.shortcuts import model_to_dict, dict_to_model

from flask import Blueprint, current_app, request, g

sys.path.insert(0, '..')

from models import *
from api_exceptions import NoSuchData

bp_weekly_meals = Blueprint(
    name='weekly_meals',
    import_name=__name__,
    url_prefix='/weekly_meals'
)

@bp_weekly_meals.route('/', methods=['GET', 'POST'])
def handle_new_weekly_meals():
    if request.method == 'GET':
        hf_week =  request.args.get('hf_week')
        date = request.args.get('date', type=int)
        meal_size = request.args.get('meal_size', 3)
        default = True if request.args.get('default') == 'true' else False

        if hf_week is None and date is None:
            hf_week = get_hf_week(20201110)
            # hf_week = get_hf_week(get_today_sk_date())
        elif hf_week is None:
            hf_week = get_hf_week(date)
        elif date is None:
            pass
        else:
            raise ValueError("Please specify either one of hf_week or date parameters. By default we get the HelloFresh week of today's date.")

        avg_rating = fn.AVG(RecipeRating.rating)
        HellofreshWeeks = (
            DateDimension
                .select(
                    DateDimension.hellofresh_week.alias("hellofresh_week")
                )
                .group_by(DateDimension.hellofresh_week)
        )

        current_app.logger.info(f"HellofreshWeeks: {model_to_dict(HellofreshWeeks[0])}")
        weekly_meals = (
            WeeklyMeals
                .select()
                .join(
                    HellofreshWeeks,
                    JOIN.LEFT_OUTER,
                    on=(HellofreshWeeks.hellofresh_week == WeeklyMeals.hellofresh_week)
                )
                # .where(
                #     (HellofreshWeeks.hellofresh_week == hf_week) |
                #     (WeeklyMeals.default_meal == default)
                # )
                # .join(
                #     RecipeRating
                #         .select(
                #             RecipeRating.fk_recipe,
                #             avg_rating.alias("avg_rating")
                #         )
                #         .group_by(RecipeRating.fk_recipe),
                #     JOIN.LEFT_OUTER,
                #     on=(WeeklyMeals.fk_recipe == RecipeRating.fk_recipe)
                # )
                # .order_by(avg_rating.desc())
                # .limit(meal_size)
        )
        current_app.logger.info(f"weekly_meals: {weekly_meals}")
        current_app.logger.info(f"weekly_meals: {weekly_meals}")

        # for meal in weekly_meals:
        #     print(model_to_dict(meal))
        # return model_to_dict(weekly_meals[0]), 200
        # weekly_meals_arr = {
        #     r.fk_recipe: model_to_dict(r, recurse=False) for r in weekly_meals
        # }

        # return json.dumps(weekly_meals_arr), 200

def get_today_sk_date():
    return datetime.strftime(datetime.today(), format="%Y%m%d")

def get_hf_week(fk_date=None):
    todays_date = get_today_sk_date() if fk_date is None else fk_date

    curr_hf_week = (
        DateDimension
            .select(DateDimension.hellofresh_week)
            .where(DateDimension.sk_date == todays_date)
            .get()
    )
    return curr_hf_week.hellofresh_week
