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

        hf_week = '2020-W46'

        # AvgRating_cte = (
        #     RecipeRating
        #         .select(
        #             RecipeRating.fk_recipe,
        #             fn.AVG(RecipeRating.rating).alias("avg_rating")
        #         )
        #         .group_by(RecipeRating.fk_recipe)
        #         .cte("AvgRating_cte", columns=('fk_recipe', 'avg_rating'))
        # )

        # AvgRating = (
        #     RecipeRating
        #         .select(
        #             RecipeRating.fk_recipe.alias("fk_recipe"),
        #             fn.AVG(RecipeRating.rating).alias("avg_rating")
        #         )
        #         .group_by(RecipeRating.fk_recipe)
        #         .alias("AvgRating")
        # )
        # test = AvgRating.execute()

        # for t in AvgRating:
        #     print(t.avg_rating)

        #     print({
        #         "fk_recipe": t.fk_recipe.sk_recipe,
        #         "avg_rating": t.avg_rating
        #         })

        # testing = (
        #     WeeklyMeals
        #         .select(
        #             WeeklyMeals
        #             # AvgRating.c.fk_recipe,
        #             AvgRating.c.avg_rating
        #         )
        #         .join(
        #             AvgRating,
        #             JOIN.LEFT_OUTER,
        #             on=(WeeklyMeals.fk_recipe == AvgRating.c.fk_recipe)
        #         )
        #         .where(
        #             (WeeklyMeals.hellofresh_week == hf_week) &
        #             (WeeklyMeals.default_meal == default)
        #         )
        #         .order_by(AvgRating.c.avg_rating.desc())
        # )
        # testing = testing.execute()

        meals = (
            WeeklyMeals
                .select()
                .where(
                    (WeeklyMeals.hellofresh_week == hf_week) &
                    (WeeklyMeals.default_meal == default)
                )
                .alias("meals")
        )
        avg_ratings = (
            RecipeRating
                .select(
                    RecipeRating.fk_recipe.alias("fk_recipe"),
                    fn.AVG(RecipeRating.rating).alias("avg_rating")
                )
                .group_by(RecipeRating.fk_recipe)
                .alias("AvgRating")
        )

        avg_rating = fn.AVG(RecipeRating.rating)

        testing = (
            WeeklyMeals
                .select(
                    WeeklyMeals.fk_recipe,
                    fn.AVG(RecipeRating.rating).alias("avg_rating")
                )
                .join(
                    RecipeRating,
                    JOIN.LEFT_OUTER,
                    on=(WeeklyMeals.fk_recipe == RecipeRating.fk_recipe)
                )
                # .where(
                #     (WeeklyMeals.hellofresh_week == hf_week) &
                #     (WeeklyMeals.default_meal == default)
                # )
                .group_by(WeeklyMeals.fk_recipe)
                .order_by(avg_rating.desc())
        )
        current_app.logger.info(f"testing.sql(): {testing.sql()}")
        testing = testing.execute()

        # current_app.logger.info(f"weekly_meals.sql(): {weekly_meals.sql()}")
        current_app.logger.info(f"hf_week: {hf_week}")

        for meal in testing:
            print(model_to_dict(meal))
            print(f"meal: {meal}")
            print(f"meal.fk_recipe: {meal.fk_recipe}")
            print(f"meal.hellofresh_week: {meal.hellofresh_week}")
            print(f"meal.avg_rating: {meal.avg_rating}")
            # print({
            #     "fk_recipe": meal.fk_recipe.sk_recipe,
            #     "avg_rating": meal.avg_rating,
            #     "hellofresh_week": meal.hellofresh_week,
            #     "default_meal": default_meal
            # })
        # weekly_meals_arr = {
        #     r.fk_recipe: model_to_dict(r, recurse=False) for r in weekly_meals
        # }

        # return json.dumps(weekly_meals_arr), 200

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
