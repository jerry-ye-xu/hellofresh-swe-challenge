from create_tables import *

if __name__ == "__main__":
    psql_db = PostgresqlDatabase(
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT']
    )
    psql_db.connect()


    ####################
    # Dimension Tables #
    ####################

    # 20201101 is a Sunday
    DateDimension.create(sk_date=20201101, hellofresh_week='2020-W46')
    DateDimension.create(sk_date=20201102, hellofresh_week='2020-W46')
    DateDimension.create(sk_date=20201103, hellofresh_week='2020-W46')
    DateDimension.create(sk_date=20201104, hellofresh_week='2020-W46')
    DateDimension.create(sk_date=20201105, hellofresh_week='2020-W46')
    DateDimension.create(sk_date=20201106, hellofresh_week='2020-W46')
    DateDimension.create(sk_date=20201107, hellofresh_week='2020-W47')
    DateDimension.create(sk_date=20201108, hellofresh_week='2020-W47')
    DateDimension.create(sk_date=20201109, hellofresh_week='2020-W47')
    DateDimension.create(sk_date=20201110, hellofresh_week='2020-W47')
    DateDimension.create(sk_date=20201111, hellofresh_week='2020-W47')
    DateDimension.create(sk_date=20201112, hellofresh_week='2020-W47')
    DateDimension.create(sk_date=20201113, hellofresh_week='2020-W47')
    DateDimension.create(sk_date=20201114, hellofresh_week='2020-W48')
    DateDimension.create(sk_date=20201115, hellofresh_week='2020-W48')
    DateDimension.create(sk_date=20201116, hellofresh_week='2020-W48')
    DateDimension.create(sk_date=20201117, hellofresh_week='2020-W48')

    CookingDifficultyDimension.create(sk_difficulty='easy')
    CookingDifficultyDimension.create(sk_difficulty='medium')
    CookingDifficultyDimension.create(sk_difficulty='hard')

    RecipeDimension.create(
        recipe_name="Southeast Asian Chicken Coconut Soup",
        recipe_subname="with Makrut Lime & Noodles",
        preparation_time=35,
        fk_difficulty='easy'
    )
    RecipeDimension.create(
        recipe_name="Saucy Coconut & Chicken Noodles",
        recipe_subname="with Lemongrass & Ginger",
        preparation_time=45,
        fk_difficulty='easy'
    )
    RecipeDimension.create(
        recipe_name="Dukkah Roasted Sweet Potato",
        recipe_subname="with Lemon Yoghurt & Mint | Serves 2",
        preparation_time=30,
        fk_difficulty='easy'
    )
    RecipeDimension.create(
        recipe_name="Chicken Tenders & Crushed Lemon Potatoes",
        recipe_subname="with Herbed Yoghurt Sauce",
        preparation_time=30,
        fk_difficulty='easy'
    )
    RecipeDimension.create(
        recipe_name="Smokey Beef Cheeseburger",
        recipe_subname="with BBQ Mayo & Paprika Fries",
        preparation_time=40,
        fk_difficulty='easy'
    )
    RecipeDimension.create(
        recipe_name="Caribbean Chicken Tacos",
        recipe_subname="with Pineapple & Cucumber Salsa",
        preparation_time=25,
        fk_difficulty='easy'
    )
    RecipeDimension.create(
        recipe_name="Beef & Basil Pesto Meatballs",
        recipe_subname="with Spaghetti & Parmesan",
        preparation_time=45,
        fk_difficulty='easy'
    )
    RecipeDimension.create(
        recipe_name="Korean Pork Bibimbap",
        recipe_subname="with Black Sesame Rice & Sugar Snap Peas",
        preparation_time=35,
        fk_difficulty='easy'
    )

    NutrientDimension.create(nutrient="Energy", measurement="kJ")
    NutrientDimension.create(nutrient="Fat", measurement="g")
    NutrientDimension.create(nutrient="Saturated", measurement="g")
    NutrientDimension.create(nutrient="Carbohydrate", measurement="g")
    NutrientDimension.create(nutrient="Sugar", measurement="g")
    NutrientDimension.create(nutrient="Dietary Fiber", measurement="g")
    NutrientDimension.create(nutrient="Protein", measurement="g")
    NutrientDimension.create(nutrient="Cholesterol", measurement="mg")
    NutrientDimension.create(nutrient="Sodium", measurement="mg")

    IngredientDimension.create(ingredient="garlic")
    IngredientDimension.create(ingredient="carrot")
    IngredientDimension.create(ingredient="Asian greens")
    IngredientDimension.create(ingredient="Southeast Asian Spice Blend")
    IngredientDimension.create(ingredient="udon noodles")
    IngredientDimension.create(ingredient="crushed peanuts")
    IngredientDimension.create(ingredient="makrut lime leaves")
    IngredientDimension.create(ingredient="capsicum")
    IngredientDimension.create(ingredient="chicken tenderloins")
    IngredientDimension.create(ingredient="coconut milk")
    IngredientDimension.create(ingredient="coriander")
    IngredientDimension.create(ingredient="olive oil")
    IngredientDimension.create(ingredient="soy sauce")
    IngredientDimension.create(ingredient="water")
    IngredientDimension.create(ingredient="brown sugar")

    IngredientDimension.create(ingredient="chicken thighs")
    IngredientDimension.create(ingredient="ginger lemongrass paste")
    IngredientDimension.create(ingredient="lime")
    IngredientDimension.create(ingredient="flat noodles")
    IngredientDimension.create(ingredient="oyster sauce")

    IngredientDimension.create(ingredient="sweet potato")
    IngredientDimension.create(ingredient="dukkah")
    IngredientDimension.create(ingredient="lemon")
    IngredientDimension.create(ingredient="long red chilli")
    IngredientDimension.create(ingredient="red onion")
    IngredientDimension.create(ingredient="flaked almonds")
    IngredientDimension.create(ingredient="mint")
    IngredientDimension.create(ingredient="Greek-style yoghurt")
    IngredientDimension.create(ingredient="honey")

    IngredientDimension.create(ingredient="potatoes")
    IngredientDimension.create(ingredient="cherry tomatoes")
    IngredientDimension.create(ingredient="chicken stock")
    IngredientDimension.create(ingredient="Dijon mustard")
    IngredientDimension.create(ingredient="dill & parsley mayonnaise")
    IngredientDimension.create(ingredient="mixed salad leaves")
    IngredientDimension.create(ingredient="butter")

    IngredientDimension.create(ingredient="brown onion")
    IngredientDimension.create(ingredient="cos lettuce leaves")
    IngredientDimension.create(ingredient="beef mince")
    IngredientDimension.create(ingredient="shredded Cheddar cheese")
    IngredientDimension.create(ingredient="BBQ mayonnaise")
    IngredientDimension.create(ingredient="paprika spice blend")
    IngredientDimension.create(ingredient="tomato")
    IngredientDimension.create(ingredient="All-American spice splend")
    IngredientDimension.create(ingredient="fine breadcrumbs")
    IngredientDimension.create(ingredient="bake-at-home burger buns")
    IngredientDimension.create(ingredient="balsamic vinegar")
    IngredientDimension.create(ingredient="salt")
    IngredientDimension.create(ingredient="eggs")

    IngredientDimension.create(ingredient="cucumber")
    IngredientDimension.create(ingredient="mild Caribbean jerk seasoning")
    IngredientDimension.create(ingredient="mayonnaise")
    IngredientDimension.create(ingredient="pineapple slices")
    IngredientDimension.create(ingredient="cos lettuce")
    IngredientDimension.create(ingredient="mini flour tortillas")

    IngredientDimension.create(ingredient="basil")
    IngredientDimension.create(ingredient="basil pesto")
    IngredientDimension.create(ingredient="dried oregano")
    IngredientDimension.create(ingredient="beef stock")
    IngredientDimension.create(ingredient="grated Parmesan cheese")
    IngredientDimension.create(ingredient="zucchini")
    IngredientDimension.create(ingredient="spaghetti pasta")
    IngredientDimension.create(ingredient="passata")
    IngredientDimension.create(ingredient="baby spinach leaves")

    IngredientDimension.create(ingredient="basmati rice")
    IngredientDimension.create(ingredient="ginger")
    IngredientDimension.create(ingredient="chilli flakes")
    IngredientDimension.create(ingredient="pork mince")
    IngredientDimension.create(ingredient="sugar snap peas")
    IngredientDimension.create(ingredient="black sesame seeds")
    IngredientDimension.create(ingredient="garlic aioli")

    ###############
    # Fact Tables #
    ###############



    psql_db.commit()
    psql_db.close()

    print("Connection to PostgreSQL in populate_tables.py has been closed.")