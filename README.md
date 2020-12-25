## Table of Contents

- [Table of Contents](#table-of-contents)
- [Setup](#setup)
- [Schema Design](#schema-design)
- [Connecting to PostgreSQL](#connecting-to-postgresql)
- [.env File](#env-file)
- [Useful resources](#useful-resources)
- [Worklog](#worklog)

## Setup

Please export the following environment variables locally.

```bash
export VERSION=$(cat VERSION)
export $(egrep -v '^#' env_var_local | xargs)
```

Note: If you open a new tab in terminal you will also need to run this again.


## Schema Design

- The "included_in_delivery" column was placed in the `recipe_dimension` table. From looking at the website, it appears that the ingredients that are not included is consistent throughout the recipes.

The following information about recipes we did not include:

- urls/src to the images of ingredients/recipes/instructions (on the website)
- warnings about ingredients with potential allergies e.g. "contain sesame, gluten may be present".
- Information about the utensils.
- Extract instructions of the recipes (I used lorem ipsum).
- Serving sizes of 2 and 4. I would effectively create a new column called "serving size", and so whenever you need a particular serving size, you just filter on that column.

## Connecting to PostgreSQL

You can connect to the PostgreSQL container locally by running

```bash
make psql_conn
```
and typing in the password.

## .env File

The PostgreSQL image requires exact naming of certain environment variables, and that the "host" may differ depending on which container we are referencing.

For the PostgreSQL image, the host should be 'localhost' and it must be set as the ENV variable `POSTGRES_HOST`. Since the Flask app is talking to the database from a different container, that is why we have 2 different ENV variables in the `env_var` file.

Please see `env_var`. We put the environment variables for flask in `env_var` as well.

For the sake of this exercise, we upload the `env_var` file for the reader to view.

<br>
<br>

---

## Worklog

- 0.0.4: 24/12/20 - Set up Flask structure including blueprints, models etc. Test simple GET method to retrieve recipes.
- 0.0.3: 22/12/20 - Insert fake data into the tables, add reasons for omitting certain details.
- 0.0.2: 21/12/20 - Create Makefile, scripts to build and teardown containers.
- 0.0.1: 20/12/20 - Initial commit of Docker files and general env setup.