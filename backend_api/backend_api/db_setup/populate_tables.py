"""
Various notes:

DateDimension: 2 weeks worth of data.
WeeklyMeals: We have 3 default meals, 4 non-default and
             1 non-weekly meal for each week.
RecipeRatings: We use random generators for the timestamp and rating value.
               The comments are also generated randomly with Bernoulli distribution p=0.2

Primary keys were included for readability (especially when constructing
the NutrientValue and Ingredient steps).
"""

from lorem_text import lorem
from random import randint, seed
from scipy import stats

from create_tables import *

seed(50)

# 2020/11/03 0:00am
START_TIMETSTAMP = 1604361600
END_TIMESTAMP = 1608595200

RATING_DIST = stats.rv_discrete(
    name='ratings_distribution',
    values=(
        [1, 2, 3, 4],
        [0.02, 0.08, 0.40, 0.50]
    )
)
PROBABILITY_COMMENT = 0.2

def random_value(start, end):
    if end <= start:
        raise ValueError("The end value must be larger than the start value.")
    diff = end - start
    while True:
        yield start + randint(0, diff)

def random_text(p, max_sentence_length):
    if stats.bernoulli.rvs(p):
        return lorem.words(max_sentence_length)
    return None

def weekly_meals_pattern_one(hellofresh_week):
    WeeklyMeals.create(
        fk_recipe=1,
        hellofresh_week=hellofresh_week,
        default_meal=True
    )
    WeeklyMeals.create(
        fk_recipe=2,
        hellofresh_week=hellofresh_week,
        default_meal=True
    )
    WeeklyMeals.create(
        fk_recipe=3,
        hellofresh_week=hellofresh_week,
        default_meal=True
    )
    WeeklyMeals.create(
        fk_recipe=4,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )
    WeeklyMeals.create(
        fk_recipe=5,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )
    WeeklyMeals.create(
        fk_recipe=6,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )
    WeeklyMeals.create(
        fk_recipe=7,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )

def weekly_meals_pattern_two(hellofresh_week):
    WeeklyMeals.create(
        fk_recipe=8,
        hellofresh_week=hellofresh_week,
        default_meal=True
    )
    WeeklyMeals.create(
        fk_recipe=7,
        hellofresh_week=hellofresh_week,
        default_meal=True
    )
    WeeklyMeals.create(
        fk_recipe=6,
        hellofresh_week=hellofresh_week,
        default_meal=True
    )
    WeeklyMeals.create(
        fk_recipe=5,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )
    WeeklyMeals.create(
        fk_recipe=4,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )
    WeeklyMeals.create(
        fk_recipe=3,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )
    WeeklyMeals.create(
        fk_recipe=2,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )

def weekly_meals_pattern_three(hellofresh_week):
    WeeklyMeals.create(
        fk_recipe=2,
        hellofresh_week=hellofresh_week,
        default_meal=True
    )
    WeeklyMeals.create(
        fk_recipe=4,
        hellofresh_week=hellofresh_week,
        default_meal=True
    )
    WeeklyMeals.create(
        fk_recipe=6,
        hellofresh_week=hellofresh_week,
        default_meal=True
    )
    WeeklyMeals.create(
        fk_recipe=5,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )
    WeeklyMeals.create(
        fk_recipe=8,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )
    WeeklyMeals.create(
        fk_recipe=3,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )
    WeeklyMeals.create(
        fk_recipe=1,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )

def weekly_meals_pattern_four(hellofresh_week):
    WeeklyMeals.create(
        fk_recipe=1,
        hellofresh_week=hellofresh_week,
        default_meal=True
    )
    WeeklyMeals.create(
        fk_recipe=3,
        hellofresh_week=hellofresh_week,
        default_meal=True
    )
    WeeklyMeals.create(
        fk_recipe=5,
        hellofresh_week=hellofresh_week,
        default_meal=True
    )
    WeeklyMeals.create(
        fk_recipe=4,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )
    WeeklyMeals.create(
        fk_recipe=8,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )
    WeeklyMeals.create(
        fk_recipe=6,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )
    WeeklyMeals.create(
        fk_recipe=7,
        hellofresh_week=hellofresh_week,
        default_meal=False
    )

def generate_month(first_date, start_idx, end_idx, hf_week, count):

    for i in range(start_idx, end_idx + 1):
        hellofresh_week = f'{str(first_date)[:4]}-W0{hf_week}' if hf_week < 10 else f'{str(first_date)[:4]}-W{hf_week}'

        DateDimension.create(
            sk_date=first_date+i,
            hellofresh_week=hellofresh_week
        )

        count += 1
        if count % 7 == 0:
            hf_week += 1


if __name__ == "__main__":
    psql_db = PostgresqlDatabase(
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['POSTGRES_HOST_FROM_BACKEND'],
        port=os.environ['POSTGRES_PORT']
    )
    psql_db.connect()


    ####################
    # Dimension Tables #
    ####################

    # 20201031 is a Saturday
    DateDimension.create(sk_date=20201031, hellofresh_week='2020-W45')

    generate_month(
        first_date=20201100,
        start_idx=1,
        end_idx=30,
        hf_week=45,
        count=1
    )

    generate_month(
        first_date=20201200,
        start_idx=1,
        end_idx=31,
        hf_week=49,
        count=3
    )

    # Handle simple edge cases, for the sake of this exercise.
    DateDimension.create(sk_date=20210101, hellofresh_week='2020-W53')

    generate_month(
        first_date=20210100,
        start_idx=2,
        end_idx=31,
        hf_week=1,
        count=0
    )

    DateDimension.create(sk_date=20210201, hellofresh_week='2021-W05')
    DateDimension.create(sk_date=20210202, hellofresh_week='2021-W05')
    DateDimension.create(sk_date=20210203, hellofresh_week='2021-W05')
    DateDimension.create(sk_date=20210204, hellofresh_week='2021-W05')
    DateDimension.create(sk_date=20210205, hellofresh_week='2021-W05')


    CookingDifficultyDimension.create(sk_difficulty='easy')
    CookingDifficultyDimension.create(sk_difficulty='medium')
    CookingDifficultyDimension.create(sk_difficulty='hard')


    #
    # Obtained from https://www.hellofresh.com.au/recipes
    #

    # Tag pt. 1
    CuisineDimension.create(sk_cuisine="Family Favourite")
    CuisineDimension.create(sk_cuisine="Turkish")
    CuisineDimension.create(sk_cuisine="American")
    CuisineDimension.create(sk_cuisine="Australian")
    CuisineDimension.create(sk_cuisine="Asian")
    CuisineDimension.create(sk_cuisine="British")
    CuisineDimension.create(sk_cuisine="Chinese")
    CuisineDimension.create(sk_cuisine="Cuban")
    CuisineDimension.create(sk_cuisine="French")
    CuisineDimension.create(sk_cuisine="German")
    CuisineDimension.create(sk_cuisine="Greek")
    CuisineDimension.create(sk_cuisine="Hawaiian")
    CuisineDimension.create(sk_cuisine="Indian")
    CuisineDimension.create(sk_cuisine="Indonesian")
    CuisineDimension.create(sk_cuisine="Irish")

    # Tag pt. 2
    CuisineDimension.create(sk_cuisine="Italian")
    CuisineDimension.create(sk_cuisine="Japanese")
    CuisineDimension.create(sk_cuisine="Korean")
    CuisineDimension.create(sk_cuisine="Lebanese")
    CuisineDimension.create(sk_cuisine="Mediterrean")
    CuisineDimension.create(sk_cuisine="Mexican")
    CuisineDimension.create(sk_cuisine="Middle Eastern")
    CuisineDimension.create(sk_cuisine="Moroccan")
    CuisineDimension.create(sk_cuisine="North African")
    CuisineDimension.create(sk_cuisine="Portuguese")
    CuisineDimension.create(sk_cuisine="Spanish")
    CuisineDimension.create(sk_cuisine="Russian")
    CuisineDimension.create(sk_cuisine="Singaporean")
    CuisineDimension.create(sk_cuisine="Thai")
    CuisineDimension.create(sk_cuisine="Vietnamese")


    RecipeDimension.create(
        # sk_recipe=1,
        recipe_name="Southeast Asian Chicken Coconut Soup",
        recipe_subname="with Makrut Lime & Noodles",
        preparation_time=35,
        fk_difficulty='easy',
        fk_cuisine='Asian'
    )
    RecipeDimension.create(
        # sk_recipe=2,
        recipe_name="Saucy Coconut & Chicken Noodles",
        recipe_subname="with Lemongrass & Ginger",
        preparation_time=45,
        fk_difficulty='easy',
        fk_cuisine='Asian'
    )
    RecipeDimension.create(
        # sk_recipe=3,
        recipe_name="Dukkah Roasted Sweet Potato",
        recipe_subname="with Lemon Yoghurt & Mint | Serves 2",
        preparation_time=30,
        fk_difficulty='easy',
        fk_cuisine='Middle Eastern'
    )
    RecipeDimension.create(
        # sk_recipe=4,
        recipe_name="Chicken Tenders & Crushed Lemon Potatoes",
        recipe_subname="with Herbed Yoghurt Sauce",
        preparation_time=30,
        fk_difficulty='easy',
        fk_cuisine='American'
    )
    RecipeDimension.create(
        # sk_recipe=5,
        recipe_name="Smokey Beef Cheeseburger",
        recipe_subname="with BBQ Mayo & Paprika Fries",
        preparation_time=40,
        fk_difficulty='easy',
        fk_cuisine='American'
    )
    RecipeDimension.create(
        # sk_recipe=6,
        recipe_name="Caribbean Chicken Tacos",
        recipe_subname="with Pineapple & Cucumber Salsa",
        preparation_time=25,
        fk_difficulty='easy',
        fk_cuisine='American'
    )
    RecipeDimension.create(
        # sk_recipe=7,
        recipe_name="Beef & Basil Pesto Meatballs",
        recipe_subname="with Spaghetti & Parmesan",
        preparation_time=45,
        fk_difficulty='easy',
        fk_cuisine='American'
    )
    RecipeDimension.create(
        # sk_recipe=8,
        recipe_name="Korean Pork Bibimbap",
        recipe_subname="with Black Sesame Rice & Sugar Snap Peas",
        preparation_time=35,
        fk_difficulty='easy',
        fk_cuisine='Korean'
    )


    NutrientDimension.create(
        # sk_nutrient=1,
        nutrient="Energy",
        measurement="kJ")
    NutrientDimension.create(
        # sk_nutrient=2,
        nutrient="Fat",
        measurement="g"
    )
    NutrientDimension.create(
        # sk_nutrient=3,
        nutrient="Saturated",
        measurement="g"
    )
    NutrientDimension.create(
        # sk_nutrient=4,
        nutrient="Carbohydrate",
        measurement="g"
    )
    NutrientDimension.create(
        # sk_nutrient=5,
        nutrient="Sugar",
        measurement="g"
    )
    NutrientDimension.create(
        # sk_nutrient=6,
        nutrient="Dietary Fiber",
        measurement="g"
    )
    NutrientDimension.create(
        # sk_nutrient=7,
        nutrient="Protein",
        measurement="g"
    )
    NutrientDimension.create(
        # sk_nutrient=8,
        nutrient="Cholesterol",
        measurement="mg"
    )
    NutrientDimension.create(
        # sk_nutrient=9,
        nutrient="Sodium",
        measurement="mg"
    )

    IngredientDimension.create(
        # sk_ingredient=1,
        ingredient="garlic"
    )
    IngredientDimension.create(
        # sk_ingredient=2,
        ingredient="carrot"
    )
    IngredientDimension.create(
        # sk_ingredient=3,
        ingredient="Asian greens"
    )
    IngredientDimension.create(
        # sk_ingredient=4,
        ingredient="Southeast Asian Spice Blend"
    )
    IngredientDimension.create(
        # sk_ingredient=5,
        ingredient="udon noodles"
    )
    IngredientDimension.create(
        # sk_ingredient=6,
        ingredient="crushed peanuts"
    )
    IngredientDimension.create(
        # sk_ingredient=7,
        ingredient="makrut lime leaves"
    )
    IngredientDimension.create(
        # sk_ingredient=8,
        ingredient="capsicum"
    )
    IngredientDimension.create(
        # sk_ingredient=9,
        ingredient="chicken tenderloins"
    )
    IngredientDimension.create(
        # sk_ingredient=10,
        ingredient="coconut milk"
    )
    IngredientDimension.create(
        # sk_ingredient=11,
        ingredient="coriander"
    )
    IngredientDimension.create(
        # sk_ingredient=12,
        ingredient="olive oil",
        included_in_delivery=False
    )
    IngredientDimension.create(
        # sk_ingredient=13,
        ingredient="soy sauce",
        included_in_delivery=False
    )
    IngredientDimension.create(
        # sk_ingredient=14,
        ingredient="water",
        included_in_delivery=False
    )
    IngredientDimension.create(
        # sk_ingredient=15,
        ingredient="brown sugar",
        included_in_delivery=False
    )

    IngredientDimension.create(
        # sk_ingredient=16,
        ingredient="chicken thighs"
    )
    IngredientDimension.create(
        # sk_ingredient=17,
        ingredient="ginger lemongrass paste"
    )
    IngredientDimension.create(
        # sk_ingredient=18,
        ingredient="lime"
    )
    IngredientDimension.create(
        # sk_ingredient=19,
        ingredient="flat noodles"
    )
    IngredientDimension.create(
        # sk_ingredient=20,
        ingredient="oyster sauce"
    )

    IngredientDimension.create(
        # sk_ingredient=21,
        ingredient="sweet potato"
    )
    IngredientDimension.create(
        # sk_ingredient=22,
        ingredient="dukkah"
    )
    IngredientDimension.create(
        # sk_ingredient=23,
        ingredient="lemon"
    )
    IngredientDimension.create(
        # sk_ingredient=24,
        ingredient="long red chilli"
    )
    IngredientDimension.create(
        # sk_ingredient=25,
        ingredient="red onion"
    )
    IngredientDimension.create(
        # sk_ingredient=26,
        ingredient="flaked almonds"
    )
    IngredientDimension.create(
        # sk_ingredient=27,
        ingredient="mint"
    )
    IngredientDimension.create(
        # sk_ingredient=28,
        ingredient="Greek-style yoghurt"
    )
    IngredientDimension.create(
        # sk_ingredient=29,
        ingredient="honey",
        included_in_delivery=False
    )

    IngredientDimension.create(
        # sk_ingredient=30,
        ingredient="potatoes"
    )
    IngredientDimension.create(
        # sk_ingredient=31,
        ingredient="cherry tomatoes"
    )
    IngredientDimension.create(
        # sk_ingredient=32,
        ingredient="chicken stock"
    )
    IngredientDimension.create(
        # sk_ingredient=33,
        ingredient="Dijon mustard"
    )
    IngredientDimension.create(
        # sk_ingredient=34,
        ingredient="dill & parsley mayonnaise"
    )
    IngredientDimension.create(
        # sk_ingredient=35,
        ingredient="mixed salad leaves"
    )
    IngredientDimension.create(
        # sk_ingredient=36,
        ingredient="butter",
        included_in_delivery=False
    )

    IngredientDimension.create(
        # sk_ingredient=37,
        ingredient="brown onion"
    )
    IngredientDimension.create(
        # sk_ingredient=38,
        ingredient="cos lettuce leaves"
    )
    IngredientDimension.create(
        # sk_ingredient=39,
        ingredient="beef mince"
    )
    IngredientDimension.create(
        # sk_ingredient=40,
        ingredient="shredded Cheddar cheese"
    )
    IngredientDimension.create(
        # sk_ingredient=41,
        ingredient="BBQ mayonnaise"
    )
    IngredientDimension.create(
        # sk_ingredient=42,
        ingredient="paprika spice blend"
    )
    IngredientDimension.create(
        # sk_ingredient=43,
        ingredient="tomato"
    )
    IngredientDimension.create(
        # sk_ingredient=44,
        ingredient="All-American spice splend"
    )
    IngredientDimension.create(
        # sk_ingredient=45,
        ingredient="fine breadcrumbs"
    )
    IngredientDimension.create(
        # sk_ingredient=46,
        ingredient="bake-at-home burger buns"
    )
    IngredientDimension.create(
        # sk_ingredient=47,
        ingredient="salt",
        included_in_delivery=False
    )
    IngredientDimension.create(
        # sk_ingredient=48,
        ingredient="balsamic vinegar",
        included_in_delivery=False
    )
    IngredientDimension.create(
        # sk_ingredient=49,
        ingredient="eggs",
        included_in_delivery=False
    )

    IngredientDimension.create(
        # sk_ingredient=50,
        ingredient="cucumber"
    )
    IngredientDimension.create(
        # sk_ingredient=51,
        ingredient="mild Caribbean jerk seasoning"
    )
    IngredientDimension.create(
        # sk_ingredient=52,
        ingredient="mayonnaise"
    )
    IngredientDimension.create(
        # sk_ingredient=53,
        ingredient="pineapple slices"
    )
    IngredientDimension.create(
        # sk_ingredient=54,
        ingredient="cos lettuce"
    )
    IngredientDimension.create(
        # sk_ingredient=55,
        ingredient="mini flour tortillas"
    )
    IngredientDimension.create(
        # sk_ingredient=56,
        ingredient="vinegar (either balsamic or white wine)",
        included_in_delivery=False
    )

    IngredientDimension.create(
        # sk_ingredient=57,
        ingredient="basil"
    )
    IngredientDimension.create(
        # sk_ingredient=58,
        ingredient="basil pesto"
    )
    IngredientDimension.create(
        # sk_ingredient=59,
        ingredient="dried oregano"
    )
    IngredientDimension.create(
        # sk_ingredient=60,
        ingredient="beef stock"
    )
    IngredientDimension.create(
        # sk_ingredient=61,
        ingredient="grated Parmesan cheese"
    )
    IngredientDimension.create(
        # sk_ingredient=62,
        ingredient="zucchini"
    )
    IngredientDimension.create(
        # sk_ingredient=63,
        ingredient="spaghetti pasta"
    )
    IngredientDimension.create(
        # sk_ingredient=64,
        ingredient="passata"
    )
    IngredientDimension.create(
        # sk_ingredient=65,
        ingredient="baby spinach leaves"
    )

    IngredientDimension.create(
        # sk_ingredient=66,
        ingredient="basmati rice"
    )
    IngredientDimension.create(
        # sk_ingredient=67,
        ingredient="ginger"
    )
    IngredientDimension.create(
        # sk_ingredient=68,
        ingredient="chilli flakes"
    )
    IngredientDimension.create(
        # sk_ingredient=69,
        ingredient="pork mince"
    )
    IngredientDimension.create(
        # sk_ingredient=70,
        ingredient="sugar snap peas"
    )
    IngredientDimension.create(
        # sk_ingredient=71,
        ingredient="black sesame seeds"
    )
    IngredientDimension.create(
        # sk_ingredient=72,
        ingredient="garlic aioli"
    )

    # We duplicate the 'ingredient' to allow for composite keys to hold.
    # A simple workaround for the purposes of this exercise.
    IngredientDimension.create(
        # sk_ingredient=73,
        ingredient="water (for the sauce)",
        included_in_delivery=False
    )
    IngredientDimension.create(
        # sk_ingredient=74,
        ingredient="water (for the rice)",
        included_in_delivery=False
    )

    IngredientDimension.create(
        # sk_ingredient=75,
        ingredient="pearl couscous",
        included_in_delivery=True
    )

    IngredientDimension.create(
        # sk_ingredient=76,
        ingredient="salmon",
        included_in_delivery=True
    )

    IngredientDimension.create(
        # sk_ingredient=77,
        ingredient="beetroot",
        included_in_delivery=True
    )

    IngredientDimension.create(
        # sk_ingredient=78,
        ingredient="smoked paprika",
        included_in_delivery=True
    )

    IngredientDimension.create(
        # sk_ingredient=79,
        ingredient="vegetable stock",
        included_in_delivery=True
    )


    #############################
    # Recipe Information Tables #
    #############################

    #
    # RecipeNutrientValue
    #

    # Southeast Asian Chicken Coconut Soup
    RecipeNutrientValue.create(
        fk_recipe=1,
        fk_nutrient=1,
        value=4316,
    )
    RecipeNutrientValue.create(
        fk_recipe=1,
        fk_nutrient=2,
        value=53.5,
    )
    RecipeNutrientValue.create(
        fk_recipe=1,
        fk_nutrient=3,
        value=27.6,
    )
    RecipeNutrientValue.create(
        fk_recipe=1,
        fk_nutrient=4,
        value=57.3,
    )
    RecipeNutrientValue.create(
        fk_recipe=1,
        fk_nutrient=5,
        value=20.3,
    )
    RecipeNutrientValue.create(
        fk_recipe=1,
        fk_nutrient=6,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=1,
        fk_nutrient=7,
        value=62.4,
    )
    RecipeNutrientValue.create(
        fk_recipe=1,
        fk_nutrient=8,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=1,
        fk_nutrient=9,
        value=1702,
    )

    # Saucy Coconut & Chicken Noodles
    RecipeNutrientValue.create(
        fk_recipe=2,
        fk_nutrient=1,
        value=3097,
    )
    RecipeNutrientValue.create(
        fk_recipe=2,
        fk_nutrient=2,
        value=34.3,
    )
    RecipeNutrientValue.create(
        fk_recipe=2,
        fk_nutrient=3,
        value=14.1,
    )
    RecipeNutrientValue.create(
        fk_recipe=2,
        fk_nutrient=4,
        value=57.5,
    )
    RecipeNutrientValue.create(
        fk_recipe=2,
        fk_nutrient=5,
        value=14.9,
    )
    RecipeNutrientValue.create(
        fk_recipe=2,
        fk_nutrient=6,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=2,
        fk_nutrient=7,
        value=44.1,
    )
    RecipeNutrientValue.create(
        fk_recipe=2,
        fk_nutrient=8,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=2,
        fk_nutrient=9,
        value=1949,
    )

    # Dukkah Roasted Sweet Potato
    RecipeNutrientValue.create(
        fk_recipe=3,
        fk_nutrient=1,
        value=1894,
    )
    RecipeNutrientValue.create(
        fk_recipe=3,
        fk_nutrient=2,
        value=16.1,
    )
    RecipeNutrientValue.create(
        fk_recipe=3,
        fk_nutrient=3,
        value=3,
    )
    RecipeNutrientValue.create(
        fk_recipe=3,
        fk_nutrient=4,
        value=55.2,
    )
    RecipeNutrientValue.create(
        fk_recipe=3,
        fk_nutrient=5,
        value=29.1,
    )
    RecipeNutrientValue.create(
        fk_recipe=3,
        fk_nutrient=6,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=3,
        fk_nutrient=7,
        value=13.2,
    )
    RecipeNutrientValue.create(
        fk_recipe=3,
        fk_nutrient=8,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=3,
        fk_nutrient=9,
        value=543,
    )

    # Chicken Tenders & Crushed Lemon Potatoes
    RecipeNutrientValue.create(
        fk_recipe=4,
        fk_nutrient=1,
        value=2494,
    )
    RecipeNutrientValue.create(
        fk_recipe=4,
        fk_nutrient=2,
        value=27.9,
    )
    RecipeNutrientValue.create(
        fk_recipe=4,
        fk_nutrient=3,
        value=9.6,
    )
    RecipeNutrientValue.create(
        fk_recipe=4,
        fk_nutrient=4,
        value=35.1,
    )
    RecipeNutrientValue.create(
        fk_recipe=4,
        fk_nutrient=5,
        value=8.5,
    )
    RecipeNutrientValue.create(
        fk_recipe=4,
        fk_nutrient=6,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=4,
        fk_nutrient=7,
        value=147.3,
    )
    RecipeNutrientValue.create(
        fk_recipe=4,
        fk_nutrient=8,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=4,
        fk_nutrient=9,
        value=1113,
    )

    # Smokey Beef Cheeseburger
    RecipeNutrientValue.create(
        fk_recipe=5,
        fk_nutrient=1,
        value=4211,
    )
    RecipeNutrientValue.create(
        fk_recipe=5,
        fk_nutrient=2,
        value=45.2,
    )
    RecipeNutrientValue.create(
        fk_recipe=5,
        fk_nutrient=3,
        value=16,
    )
    RecipeNutrientValue.create(
        fk_recipe=5,
        fk_nutrient=4,
        value=88.2,
    )
    RecipeNutrientValue.create(
        fk_recipe=5,
        fk_nutrient=5,
        value=21.7,
    )
    RecipeNutrientValue.create(
        fk_recipe=5,
        fk_nutrient=6,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=5,
        fk_nutrient=7,
        value=54.1,
    )
    RecipeNutrientValue.create(
        fk_recipe=5,
        fk_nutrient=8,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=5,
        fk_nutrient=9,
        value=1687,
    )

    # Caribbean Chicken Tacos
    RecipeNutrientValue.create(
        fk_recipe=6,
        fk_nutrient=1,
        value=2609,
    )
    RecipeNutrientValue.create(
        fk_recipe=6,
        fk_nutrient=2,
        value=21.6,
    )
    RecipeNutrientValue.create(
        fk_recipe=6,
        fk_nutrient=3,
        value=2.6,
    )
    RecipeNutrientValue.create(
        fk_recipe=6,
        fk_nutrient=4,
        value=53.2,
    )
    RecipeNutrientValue.create(
        fk_recipe=6,
        fk_nutrient=5,
        value=13.3,
    )
    RecipeNutrientValue.create(
        fk_recipe=6,
        fk_nutrient=6,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=6,
        fk_nutrient=7,
        value=48.8,
    )
    RecipeNutrientValue.create(
        fk_recipe=6,
        fk_nutrient=8,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=6,
        fk_nutrient=9,
        value=1491,
    )

    # Beef & Basil Pesto Meatballs
    RecipeNutrientValue.create(
        fk_recipe=7,
        fk_nutrient=1,
        value=3636,
    )
    RecipeNutrientValue.create(
        fk_recipe=7,
        fk_nutrient=2,
        value=30.1,
    )
    RecipeNutrientValue.create(
        fk_recipe=7,
        fk_nutrient=3,
        value=12.4,
    )
    RecipeNutrientValue.create(
        fk_recipe=7,
        fk_nutrient=4,
        value=90.1,
    )
    RecipeNutrientValue.create(
        fk_recipe=7,
        fk_nutrient=5,
        value=15.1,
    )
    RecipeNutrientValue.create(
        fk_recipe=7,
        fk_nutrient=6,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=7,
        fk_nutrient=7,
        value=53,
    )
    RecipeNutrientValue.create(
        fk_recipe=7,
        fk_nutrient=8,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=7,
        fk_nutrient=9,
        value=1229,
    )

    # Korean Pork Bibimbap
    RecipeNutrientValue.create(
        fk_recipe=8,
        fk_nutrient=1,
        value=4072,
    )
    RecipeNutrientValue.create(
        fk_recipe=8,
        fk_nutrient=2,
        value=52.9,
    )
    RecipeNutrientValue.create(
        fk_recipe=8,
        fk_nutrient=3,
        value=12,
    )
    RecipeNutrientValue.create(
        fk_recipe=8,
        fk_nutrient=4,
        value=75.6,
    )
    RecipeNutrientValue.create(
        fk_recipe=8,
        fk_nutrient=5,
        value=14.2,
    )
    RecipeNutrientValue.create(
        fk_recipe=8,
        fk_nutrient=6,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=8,
        fk_nutrient=7,
        value=44.7,
    )
    RecipeNutrientValue.create(
        fk_recipe=8,
        fk_nutrient=8,
        value=0.0,
    )
    RecipeNutrientValue.create(
        fk_recipe=8,
        fk_nutrient=9,
        value=1609,
    )

    #
    # RecipeIngredient
    #

    # Southeast Asian Chicken Coconut Soup
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=1,
        value=2,
        unit="clove"
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=2,
        value=1,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=3,
        value=1,
        unit="bunch"
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=4,
        value=1.5,
        unit="sachet"
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=5,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=6,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=7,
        value=2,
        unit="leaves"
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=8,
        value=1,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=9,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=10,
        value=1,
        unit="tin"
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=11,
        value=1,
        unit="bag"
    )
    # Olive oil, amount not specified
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=12,
        value=0,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=13,
        value=2,
        unit="tbs"
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=14,
        value=1.5,
        unit="cup"
    )
    RecipeIngredient.create(
        fk_recipe=1,
        fk_ingredient=15,
        value=2,
        unit="tsp"
    )

    # Saucy Coconut & Chicken Noodles
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=1,
        value=2,
        unit="clove"
    )
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=2,
        value=1,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=16,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=17,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=10,
        value=2,
        unit="tin"
    )
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=3,
        value=1,
        unit="bunch"
    )
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=18,
        value=0.5,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=19,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=4,
        value=0.5,
        unit="sachet"
    )
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=20,
        value=1,
        unit="packet"
    )
    # Olive oil, amount not specified
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=12,
        value=0,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=15,
        value=2,
        unit="tsp"
    )
    RecipeIngredient.create(
        fk_recipe=2,
        fk_ingredient=13,
        value=2,
        unit="tsp"
    )

    # Dukkah Roasted Sweet Potato
    RecipeIngredient.create(
        fk_recipe=3,
        fk_ingredient=21,
        value=3,
        unit=""
    )
    # Accidently missed 22 when creating ingredients
    RecipeIngredient.create(
        fk_recipe=3,
        fk_ingredient=22,
        value=1,
        unit="sachet"
    )
    RecipeIngredient.create(
        fk_recipe=3,
        fk_ingredient=23,
        value=1,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=3,
        fk_ingredient=24,
        value=3,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=3,
        fk_ingredient=25,
        value=1,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=3,
        fk_ingredient=26,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=3,
        fk_ingredient=27,
        value=1,
        unit="bunch"
    )
    RecipeIngredient.create(
        fk_recipe=3,
        fk_ingredient=28,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=3,
        fk_ingredient=29,
        value=1,
        unit="tsp"
    )

    # Chicken Tenders & Crushed Lemon Potatoes
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=30,
        value=2,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=31,
        value=1,
        unit="punnet"
    )
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=32,
        value=1,
        unit="cube"
    )
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=33,
        value=0.5,
        unit="tub"
    )
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=34,
        value=0.5,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=1,
        value=2,
        unit="clove"
    )
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=23,
        value=0.5,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=9,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=35,
        value=1,
        unit="bag"
    )
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=28,
        value=0.5,
        unit="packet"
    )
    # Olive oil, amount not specified
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=12,
        value=0,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=14,
        value=1,
        unit="tbs"
    )
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=36,
        value=25,
        unit="g"
    )
    RecipeIngredient.create(
        fk_recipe=4,
        fk_ingredient=29,
        value=0.5,
        unit="tsp"
    )

    # Smokey Beef Cheeseburger
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=30,
        value=2,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=37,
        value=1,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=38,
        value=1,
        unit="bag"
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=39,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=40,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=41,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=42,
        value=0.5,
        unit="sachet"
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=43,
        value=1,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=44,
        value=1,
        unit="sachet"
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=45,
        value=0.5,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=46,
        value=2,
        unit=""
    )
    # Olive oil, amount not specified
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=12,
        value=0,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=14,
        value=2,
        unit="tsp"
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=47,
        value=0.25,
        unit="tsp"
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=48,
        value=1,
        unit="tbs"
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=15,
        value=1.5,
        unit="tsp"
    )
    RecipeIngredient.create(
        fk_recipe=5,
        fk_ingredient=49,
        value=1,
        unit=""
    )

    # Caribbean Chicken Tacos
    RecipeIngredient.create(
        fk_recipe=6,
        fk_ingredient=1,
        value=1,
        unit="clove",
    )
    RecipeIngredient.create(
        fk_recipe=6,
        fk_ingredient=50,
        value=1,
        unit="",
    )
    RecipeIngredient.create(
        fk_recipe=6,
        fk_ingredient=24,
        value=0.5,
        unit="",
    )
    RecipeIngredient.create(
        fk_recipe=6,
        fk_ingredient=51,
        value=1,
        unit="sachet",
    )
    RecipeIngredient.create(
        fk_recipe=6,
        fk_ingredient=52,
        value=1,
        unit="packet",
    )
    RecipeIngredient.create(
        fk_recipe=6,
        fk_ingredient=53,
        value=0.5,
        unit="tin",
    )
    RecipeIngredient.create(
        fk_recipe=6,
        fk_ingredient=54,
        value=0.5,
        unit="head",
    )
    RecipeIngredient.create(
        fk_recipe=6,
        fk_ingredient=9,
        value=1,
        unit="packet",
    )
    RecipeIngredient.create(
        fk_recipe=6,
        fk_ingredient=55,
        value=6,
        unit="",
    )
    # Olive oil, amount not specified
    RecipeIngredient.create(
        fk_recipe=6,
        fk_ingredient=12,
        value=0,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=6,
        fk_ingredient=56,
        value=0.5,
        unit="tsp",
    )
    RecipeIngredient.create(
        fk_recipe=6,
        fk_ingredient=47,
        value=0.25,
        unit="tsp",
    )

    # Beef & Basil Pesto Meatballs
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=37,
        value=0.5,
        unit="",
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=57,
        value=1,
        unit="punnet",
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=39,
        value=1,
        unit="packet",
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=58,
        value=1,
        unit="sachet",
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=59,
        value=0.5,
        unit="sachet",
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=60,
        value=1,
        unit="cube"
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=61,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=1,
        value=2,
        unit="clove"
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=62,
        value=1,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=45,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=63,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=64,
        value=1,
        unit="box"
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=65,
        value=1,
        unit="bag"
    )
    # Olive oil, amount not specified
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=12,
        value=0,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=49,
        value=1,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=15,
        value=2,
        unit="tsp"
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=47,
        value=0.25,
        unit="tsp"
    )
    RecipeIngredient.create(
        fk_recipe=7,
        fk_ingredient=36,
        value=10,
        unit="g"
    )

    # Korean Pork Bibimbap
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=66,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=67,
        value=1,
        unit="knob"
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=2,
        value=1,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=50,
        value=1,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=68,
        value=1,
        unit="pinch"
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=1,
        value=1,
        unit="clove"
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=69,
        value=1,
        unit="packet"
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=70,
        value=1,
        unit="bag"
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=71,
        value=0.5,
        unit="sachet"
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=72,
        value=1,
        unit="packet"
    )
    # Olive oil, amount not specified
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=12,
        value=0,
        unit=""
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=13,
        value=0.25,
        unit="cup"
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=73,
        value=1,
        unit="tbs"
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=74,
        value=1.5,
        unit="cup"
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=15,
        value=3,
        unit="tbs"
    )
    RecipeIngredient.create(
        fk_recipe=8,
        fk_ingredient=49,
        value=2,
        unit=""
    )

    #
    # RecipeInstruction
    #

    total_num_instr_for_each_recipe =[6, 6, 4, 6, 6, 6, 6, 6]
    for i in range(1, 8+1):
        for j in range(1, total_num_instr_for_each_recipe[i-1]+1):
            RecipeInstruction.create(
                fk_recipe=i,
                step=j,
                instruction=random_text(p=1, max_sentence_length=randint(1, 5))
            )

    ###############
    # Fact Tables #
    ###############

    #
    # For the purposes of this exercise, we repeat the pattern every 4 weeks.
    #

    weekly_meals_pattern_one('2020-W45')
    weekly_meals_pattern_two('2020-W46')
    weekly_meals_pattern_three('2020-W47')
    weekly_meals_pattern_four('2020-W48')
    weekly_meals_pattern_one('2020-W49')
    weekly_meals_pattern_two('2020-W50')
    weekly_meals_pattern_three('2020-W51')
    weekly_meals_pattern_four('2020-W52')
    weekly_meals_pattern_one('2020-W53')
    weekly_meals_pattern_two('2021-W01')
    weekly_meals_pattern_three('2020-W02')
    weekly_meals_pattern_four('2020-W03')
    weekly_meals_pattern_one('2021-W04')
    weekly_meals_pattern_two('2021-W05')
    weekly_meals_pattern_three('2021-W06')
    weekly_meals_pattern_four('2021-W07')


    for i in range(500):
        RecipeRating.create(
            fk_recipe=randint(1, 8),
            rating=RATING_DIST.rvs(),
            comment=random_text(
                PROBABILITY_COMMENT,
                randint(1, 15)
            ),
            timestamp=next(random_value(
                START_TIMETSTAMP,
                END_TIMESTAMP
            ))
        )

    psql_db.commit()
    psql_db.close()

    print("Connection to PostgreSQL in populate_tables.py has been closed.")