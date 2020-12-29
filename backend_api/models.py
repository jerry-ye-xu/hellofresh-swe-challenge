import os

from peewee import (
    Check,
    Model,
    PostgresqlDatabase,
    AutoField,
    BooleanField,
    CharField,
    IntegerField,
    FixedCharField,
    FloatField,
    ForeignKeyField,
    TextField,
    TimestampField
)

psql_db = PostgresqlDatabase(
    database=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ['POSTGRES_HOST_FROM_BACKEND'],
    port=os.environ['POSTGRES_PORT']
)

class BaseModel(Model):
    class Meta:
        database = psql_db


####################
# Dimension Tables #
####################

class DateDimension(BaseModel):
    # Format: yyyymmdd e.g. 20202512
    sk_date = IntegerField(primary_key=True)

    # Format: yyyy-Wdd e.g. 2020-W01
    hellofresh_week = FixedCharField(
        null=False,
        max_length=8
    )

    class Meta:
        table_name = "date_dimension"
        schema = "dimensions"

class CookingDifficultyDimension(BaseModel):
    sk_difficulty = CharField(primary_key=True)

    class Meta:
        table_name = "cooking_difficulty_dimension"
        schema = "dimensions"

class CuisineDimension(BaseModel):
    sk_cuisine = CharField(primary_key=True)

    class Meta:
        table_name = "cuisine_dimension"
        schema = "dimensions"

class RecipeDimension(BaseModel):
    sk_recipe = AutoField(primary_key=True)
    recipe_name = TextField(
        unique=True,
        null=False
    )
    recipe_subname = TextField(
        null=False
    )
    preparation_time = IntegerField(
        null=False,
        constraints=[Check('preparation_time > 0')]
    )
    fk_difficulty = ForeignKeyField(
        model=CookingDifficultyDimension,
        field="sk_difficulty"
    )
    fk_cuisine = ForeignKeyField(
        null=False,
        model=CuisineDimension,
        field="sk_cuisine"
    )

    class Meta:
        table_name = "recipe_dimension"
        schema = "dimensions"

class NutrientDimension(BaseModel):
    sk_nutrient = AutoField(primary_key=True)
    nutrient = CharField(
        unique=True,
        null=False
    )
    measurement = CharField(
        null=False
    )

    class Meta:
        table_name = "nutrient_dimension"
        schema = "dimensions"

class IngredientDimension(BaseModel):
    sk_ingredient = AutoField(primary_key=True)
    ingredient = CharField(
        unique=True,
        null=False
    )
    included_in_delivery = BooleanField(default=True)

    class Meta:
        table_name = "ingredient_dimension"
        schema = "dimensions"


#############################
# Recipe Information Tables #
#############################

class RecipeNutrientValue(BaseModel):
    sk_rec_nut = AutoField()
    fk_recipe = ForeignKeyField(
        model=RecipeDimension,
        field="sk_recipe"
    )
    fk_nutrient = ForeignKeyField(
        model=NutrientDimension,
        field="sk_nutrient"
    )

    value = FloatField(
        null=False,
        constraints=[Check('value >= 0')]
    )

    class Meta:
        table_name = "recipe_nutrient_value"
        schema = "fact_tables"

class RecipeIngredient(BaseModel):
    sk_rec_ing = AutoField()
    fk_recipe = ForeignKeyField(
        model=RecipeDimension,
        field="sk_recipe"
    )
    fk_ingredient = ForeignKeyField(
        model=IngredientDimension,
        field="sk_ingredient"
    )
    serving_size = IntegerField(null=False, default=2)
    value = FloatField(null=False)
    unit = CharField(null=False)

    class Meta:
        table_name = "recipe_ingredient"
        schema = "fact_tables"

class RecipeInstruction(BaseModel):
    sk_rec_ins = AutoField()
    fk_recipe = ForeignKeyField(
        model=RecipeDimension,
        field="sk_recipe"
    )
    step = IntegerField(null=False)
    instruction = TextField(null=False)

    class Meta:
        table_name = "recipe_instruction"
        schema = "fact_tables"


###############
# Fact Tables #
###############

class WeeklyMeals(BaseModel):
    fk_recipe = ForeignKeyField(
        model=RecipeDimension,
        field="sk_recipe"
    )
    hellofresh_week = FixedCharField(
        null=False,
        max_length=8
    )

    default_meal = BooleanField(
        null=False,
        default=False
    )

    class Meta:
        table_name = "weekly_meals"
        schema = "fact_tables"

class RecipeRating(BaseModel):
    sk_rating = AutoField(primary_key=True)
    rating = FloatField(
        null=False,
        constraints=[Check('rating >= 1.0'), Check('rating <= 4.0')]
    )
    fk_recipe = ForeignKeyField(
        model=RecipeDimension,
        field="sk_recipe"
    )
    comment = TextField(null=True)
    timestamp = TimestampField(
        null=False
    )

    class Meta:
        table_name = "recipe_rating"
        schema = "fact_tables"