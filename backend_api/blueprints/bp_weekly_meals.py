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

        # avg_rating = fn.Avg(RecipeRating.rating)
        # HellofreshWeeks = (
        #     DateDimension
        #         .select(
        #             DateDimension.hellofresh_week.alias("hellofresh_week")
        #         )
        #         .group_by(DateDimension.hellofresh_week)
        # )

        # current_app.logger.info(f"HellofreshWeeks: {HellofreshWeeks}")
        # current_app.logger.info(f"HellofreshWeeks: {model_to_dict(HellofreshWeeks[0])}")

        hf_week = '2020-W46'

        AvgRating_cte = (
            RecipeRating
                .select(
                    RecipeRating.fk_recipe,
                    fn.AVG(RecipeRating.rating).alias("avg_rating")
                )
                .group_by(RecipeRating.fk_recipe)
                .cte("AvgRating_cte", columns=('fk_recipe', 'avg_rating'))
        )

        AvgRating = (
            RecipeRating
                .select(
                    RecipeRating.fk_recipe,
                    fn.AVG(RecipeRating.rating).alias("avg_rating")
                )
                .group_by(RecipeRating.fk_recipe)
        )
        test = AvgRating.execute()

        for t in test:
            print(t.avg_rating)

            print({
                "fk_recipe": t.fk_recipe.sk_recipe,
                "avg_rating": t.avg_rating
                })

        weekly_meals = (
            WeeklyMeals
                .select(
                    WeeklyMeals,
                    AvgRating_cte.c.avg_rating
                )
                .where(
                    (WeeklyMeals.hellofresh_week == hf_week) &
                    (WeeklyMeals.default_meal == default)
                )
                .join(
                    AvgRating_cte,
                    JOIN.LEFT_OUTER,
                    on=(WeeklyMeals.fk_recipe == AvgRating_cte.c.fk_recipe)
                )
                .order_by(AvgRating_cte.c.avg_rating.desc())
                .with_cte(AvgRating_cte)
        )
        current_app.logger.info(f"weekly_meals.sql(): {weekly_meals.sql()}")

        testing = weekly_meals.execute()
        current_app.logger.info(f"hf_week: {hf_week}")

        for meal in testing:
            print(meal.avg_rating)
            print({
                "fk_recipe": meal.fk_recipe.sk_recipe,
                "avg_rating": meal.avg_rating,
                "hellofresh_week": meal.hellofresh_week,
                "default_meal": default_meal
            })
        meal = testing[0]
        return model_to_dict({
                "fk_recipe": meal.fk_recipe.sk_recipe,
                "avg_rating": meal.avg_rating,
                "hellofresh_week": meal.hellofresh_week,
                "default_meal": default_meal
            }), 200
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
