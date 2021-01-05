import sys
sys.path.insert(0, '..')

from backend_api.models import *

if __name__ == "__main__":
    dim_tables = [
        DateDimension,
        CookingDifficultyDimension,
        CuisineDimension,
        RecipeDimension,
        NutrientDimension,
        IngredientDimension,
    ]

    recipe_info_tables = [
        RecipeNutrientValue,
        RecipeIngredient,
        RecipeInstruction
    ]

    fact_tables = [
        WeeklyMeals,
        RecipeRating
    ]

    psql_db.connect()
    psql_db.create_tables(
        dim_tables +
        recipe_info_tables +
        fact_tables
    )

    psql_db.close()

    print("Connection to PostgreSQL in create_tables.py has been closed.")