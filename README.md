## Table of Contents

- [Table of Contents](#table-of-contents)
- [Setup](#setup)
- [Schema Design](#schema-design)
- [Connecting to PostgreSQL](#connecting-to-postgresql)
- [.env File](#env-file)
- [Useful resources](#useful-resources)
- [Worklog](#worklog)

## Setup



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

Note that the PostgreSQL image requires exact naming of certain environment variables, and that the "host" may differ depending on which container we are referencing.

Please see `pg_env_var`.

For the sake of this exercise, we upload the `pg_env_var` file for the reader to view.

## Useful resources

- [Using PostgreSQL image](https://hub.docker.com/_/postgres)

- [.env, ARG, ENV, env_file](https://vsupalov.com/docker-arg-env-variable-guide/)

- [src for `postgresqlDatabase` class](https://github.com/coleifer/peewee/blob/master/peewee.py)

- [ENV PYTHONUNBUFFERED=1](https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file)

- [PostgreSQL System catalog](https://severalnines.com/database-blog/understanding-and-reading-postgresql-system-catalog)

- [Bash scripts](https://stackoverflow.com/questions/34228864/stop-and-delete-docker-container-if-its-running)

- [Bash scripts pt. 2](https://stackoverflow.com/questions/12137431/test-if-a-command-outputs-an-empty-string/25496589#25496589)

- [Docker: Removing images](https://stackoverflow.com/questions/40084044/how-to-remove-docker-images-based-on-name)

- [exec in Bash](https://askubuntu.com/questions/525767/what-does-an-exec-command-do)

- [PostgreSQL CLI commands](https://www.postgresqltutorial.com/psql-commands/)

- [Wait for PostgreSQL to finish before running Flask API](https://docs.docker.com/compose/startup-order/)

- [What does Shift do in Bash](https://unix.stackexchange.com/questions/174566/what-is-the-purpose-of-using-shift-in-shell-scripts)

- [Dockerize PostgreSQL from scratch](https://docs.docker.com/engine/examples/postgresql_service/)

- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

<br>
<br>

---

## Worklog

- 0.0.3-rc: 22/12/20 - Insert fake data into the tables, add reasons for omitting certain details.
- 0.0.2-rc: 21/12/20 - Create Makefile, scripts to build and teardown containers.
- 0.0.1-rc: 20/12/20 - Initial commit of Docker files and general env setup.