## Table of Contents

- [Table of Contents](#table-of-contents)
- [Setup](#setup)
- [Schema Design](#schema-design)
- [Connecting to PostgreSQL](#connecting-to-postgresql)
- [.env File](#env-file)
- [Useful resources](#useful-resources)
- [Worklog](#worklog)

## Setup

### Step 1

Set up your local virtual environment with
```bash
virtualenv venv

# shortcut for activating virtualenv
source activate.sh

pip3 install -r requirements.txt

cd backend_api && pip3 install -e . && cd ..
```

### Step 2
Please export the following environment variables locally.

```bash
export VERSION=$(cat VERSION)
export $(egrep -v '^#' env_var_local | xargs)
```

Note: If you open a new tab in terminal you will also need to run this again.

### Step 2

Import the Postman collections for testing. The version used is `v2.1`.

To run the tests in the command line, first install the `newman` package.

```bash
npm install -g newman
```

### Step 3

To kickstart the application and run the tests, use

```bash
make build_all
```

### Step 4

Run the tests with

```bash
make run_tests
```

Please see the makefile for more.

__IMPORTANT:__ The tests are not omnipotent. If you want to repeat any steps, please start again from `build_quick` and make sure all Docker assets are deleted with `make clean_all`.

Note: To just run the application without clearing the images, use
```bash
make build_quick
```

## Schema Design

- The "included_in_delivery" column was placed in the `recipe_dimension` table. From looking at the website, it appears that the ingredients that are not included is consistent throughout the recipes.

The following information about recipes we did not include:

- urls/src to the images of ingredients/recipes/instructions (on the website)
- the description of the recipes.
- warnings about ingredients with potential allergies e.g. "contain sesame, gluten may be present".
- Information about the utensils.
- Extract instructions of the recipes (I used lorem ipsum).
- Serving sizes of 2 and 4. I would effectively create a new column called "serving size", and so whenever you need a particular serving size, you just filter on that column.

For the ER diagram, please see the __HF-SWE-ERD-design.pdf__ file.

## Connecting to PostgreSQL using CLI

You can connect to the PostgreSQL container locally by running

```bash
make psql_conn
```
and typing in the password (see `env_var_local`).

## .env File

The PostgreSQL image requires exact naming of certain environment variables, and that the "host" may differ depending on which container we are referencing.

For the PostgreSQL image, the host should be 'localhost' and it must be set as the ENV variable `POSTGRES_HOST`. Since the Flask app is talking to the database from a different container, that is why we have 2 different ENV variables in the `env_var` file.

Please see `env_var`. We put the environment variables for flask in `env_var` as well.

For the sake of this exercise, we upload the `env_var` file for the reader to view.

For local use outside of the containers, the environment variables are kept in `env_var_local`.

<br>
<br>

---

## Worklog


- 0.2.0: 05/01/21 - Change Flask structure to `backend_api/backend_api/` to allow local directory installatino to work. Add in simple pytests to showcase functionality.
- 0.1.1: 05/01/21 - Update DELETE request for recipes (to relevant information from all other dependent tables). Finalise and add POSTMAN collection.
- 0.1.0: 04/01/21 - Configure /recipes POST method to include ingredients and nutrients and instructions.
- 0.0.9: 03/01/21 - Split weekly_meals into 'non_default_meals' and 'default_meals' end points and add in checks for various cases. Finalise ER diagram.
- 0.0.8: 03/01/21 - Create tests for POSTMAN collections (except HF-recipes).
- 0.0.7: 01/01/21 - Add end point for updating rows in ingredient dimension table. Update relevant tables to use composite keys.
- 0.0.6: 30/12/20 - Add end points for updating rows in nutrient and instruction dimension tables.
- 0.0.5: 28/12/20 - Set up API for weekly_meals and recipe_ratings.
- 0.0.4: 24/12/20 - Set up Flask structure including blueprints, models etc. Test simple GET method to retrieve recipes.
- 0.0.3: 22/12/20 - Insert fake data into the tables, add reasons for omitting certain details.
- 0.0.2: 21/12/20 - Create Makefile, scripts to build and teardown containers.
- 0.0.1: 20/12/20 - Initial commit of Docker files and general env setup.
