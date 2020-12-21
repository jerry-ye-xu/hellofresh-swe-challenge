from create_tables import *

if __name__ == "__main__":
    psql_db = PostgresqlDatabase(
        database=os.environ['POSTGRES_DATABASE'],
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
        preparation_time=35,
        fk_difficulty='easy'
    )
    # RecipeDimension(
    #     recipe_name="Southeast Asian Chicken Coconut Soup",
    #     preparation_time=35,
    #     fk_difficulty='easy'
    # )
    # RecipeDimension(
    #     recipe_name="Southeast Asian Chicken Coconut Soup",
    #     preparation_time=35,
    #     fk_difficulty='easy'
    # )

    psql_db.commit()
    psql_db.close()

    print("Connection to PostgreSQL in populate_tables.py has been closed.")