"""
Authors note:

The majority of paths have been covered in the Postman collections.

Both here and in 'test_recipe_routes.py', we showcase the basic functionality of
pytest and include a few examples.
"""

from backend_api.models import *

def test_date_dimension():
    date = DateDimension(sk_date='20210105', hellofresh_week='2021-W01')

    assert date.sk_date == '20210105'
    assert date.hellofresh_week == '2021-W01'

def test_cooking_difficulty_dimension():
    difficulty = CookingDifficultyDimension(sk_difficulty='hard', hellofresh_week='2021-W01')

    assert difficulty.sk_difficulty == 'hard'

def test_cuisine_dimension():
    cuisine = CuisineDimension(sk_cuisine="American")

    assert cuisine.sk_cuisine == "American"

def test_recipe_dimension():
    recipe = RecipeDimension(
        recipe_name="new-recipe",
        recipe_subname="new-subname",
        preparation_time=30,
        fk_difficulty='hard',
        fk_cuisine='Korean'
    )

    assert recipe.recipe_name == "new-recipe"
    assert recipe.recipe_subname == "new-subname"
    assert recipe.preparation_time == 30
    assert recipe.fk_difficulty.sk_difficulty == 'hard'
    assert recipe.fk_cuisine.sk_cuisine == 'Korean'

def test_nutrient_dimension():
    nutrient = NutrientDimension(
        nutrient="new-nutrient",
        measurement="mg",
    )

    assert nutrient.nutrient == "new-nutrient"
    assert nutrient.measurement == "mg"

def test_ingredient_dimension():
    ingredient = IngredientDimension(
        ingredient="new-ingredient",
        included_in_delivery=False
    )

    assert ingredient.ingredient == 'new-ingredient'
    assert ingredient.included_in_delivery == False

def test_recipe_nutrient_value():
    nutrient_value = RecipeNutrientValue(
        fk_recipe=1,
        fk_nutrient=3,
        value=5
    )

    assert nutrient_value.fk_recipe.sk_recipe == 1
    assert nutrient_value.fk_nutrient.sk_nutrient == 3
    assert nutrient_value.value == 5

def test_recipe_ingredient():
    recipe_ingredient = RecipeIngredient(
        fk_recipe=1,
        fk_ingredient=3,
        serving_size=2,
        value=1,
        unit=""
    )

    assert recipe_ingredient.fk_recipe.sk_recipe == 1
    assert recipe_ingredient.fk_ingredient.sk_ingredient == 3
    assert recipe_ingredient.serving_size == 2
    assert recipe_ingredient.value == 1
    assert recipe_ingredient.unit == ""

def test_recipe_instruction():
    recipe_instruction = RecipeInstruction(
        fk_recipe=1,
        step=2,
        instruction="A new instruction."
    )

    assert recipe_instruction.fk_recipe.sk_recipe == 1
    assert recipe_instruction.step == 2
    assert recipe_instruction.instruction == "A new instruction."

def test_weekly_meals():
    weekly_meal = WeeklyMeals(
        fk_recipe=1,
        hellofresh_week="2021-W01",
        default_meal=False
    )

    assert weekly_meal.fk_recipe.sk_recipe == 1
    assert weekly_meal.hellofresh_week == "2021-W01"
    assert weekly_meal.default_meal== False

def test_recipe_rating():
    rating = RecipeRating(
        fk_recipe=1,
        rating=4,
        comment="It was delicious!",
        timestamp=10000000
    )
    assert rating.fk_recipe.sk_recipe == 1
    assert rating.rating == 4
    assert rating.comment == "It was delicious!"
    assert rating.timestamp == 10000000