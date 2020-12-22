## PG STATS TABLES

The following are some of the tables stored by PostgreSQL System Catalog

- pg_stat_database
- pg_stat_bgwriter
- pg_stat_activity
- pg_locks
- pg_stat_user_tables
- pg_statio_user_tables
- pg_stat_user_indexes

To see all the tables available:

```SQL
SELECT * FROM information_schema.tables;
```

The 3 default schemas are:

- **pg_catalog**
- **information_schema**
- **public** (default if new tables are created without specifying a schema)

To see tables for a particular schema you can use either pg_catalog or information_schema:

```SQL
SELECT *
    FROM pg_catalog.pg_tables
        WHERE schemaname = 'dimensions';
```

```SQL
SELECT *
    FROM information_schema.tables
        WHERE table_schema = 'dimensions';
```

In order to create a new schema simply:

```SQL
CREATE SCHEMA IF NOT EXISTS new_schema;
```

## TABLE CHECK COMMANDS

```SQL
SELECT * FROM dimensions.date_dimension;
SELECT * FROM dimensions.cooking_difficulty_dimension;
SELECT * FROM dimensions.recipe_dimension;
SELECT * FROM dimensions.nutrient_dimension;
SELECT * FROM dimensions.ingredient_dimension;

SELECT * FROM fact_tables.recipe_nutrient_value;
SELECT * FROM fact_tables.recipe_ingredient;
SELECT * FROM fact_tables.recipe_instruction;

SELECT * FROM fact_tables.weekly_meals;
SELECT * FROM fact_tables.recipe_rating;
```