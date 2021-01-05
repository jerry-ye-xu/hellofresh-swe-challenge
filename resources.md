## Useful resources

- [Using PostgreSQL image](https://hub.docker.com/_/postgres)

- [.env, ARG, ENV, env_file](https://vsupalov.com/docker-arg-env-variable-guide/)

- [ARG vs. ENV](https://vsupalov.com/docker-build-pass-environment-variables/)

- [src for `postgresqlDatabase` class](https://github.com/coleifer/peewee/blob/master/peewee.py)

- [ENV PYTHONUNBUFFERED=1](https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file)

- [PostgreSQL System catalog](https://severalnines.com/database-blog/understanding-and-reading-postgresql-system-catalog)

- [Bash scripts](https://stackoverflow.com/questions/34228864/stop-and-delete-docker-container-if-its-running)

- [Bash scripts pt. 2](https://stackoverflow.com/questions/12137431/test-if-a-command-outputs-an-empty-string/25496589#25496589)

- [Docker compose V3 reference](https://docs.docker.com/compose/compose-file/compose-file-v3/)

- [Docker: Removing images](https://stackoverflow.com/questions/40084044/how-to-remove-docker-images-based-on-name)

- [Docker container prune](https://docs.docker.com/engine/reference/commandline/container_prune/)

- [exec in Bash](https://askubuntu.com/questions/525767/what-does-an-exec-command-do)

- [PostgreSQL CLI commands](https://www.postgresqltutorial.com/psql-commands/)

- [Wait for PostgreSQL to finish before running Flask API](https://docs.docker.com/compose/startup-order/)

- [What does Shift do in Bash](https://unix.stackexchange.com/questions/174566/what-is-the-purpose-of-using-shift-in-shell-scripts)

- [Dockerize PostgreSQL from scratch](https://docs.docker.com/engine/examples/postgresql_service/)

- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

- [Useful Docker asset management commands](https://phoenixnap.com/kb/remove-docker-images-containers-networks-volumes)

- [Useful Docker asset management commands 2](https://linuxize.com/post/how-to-remove-docker-images-containers-volumes-and-networks/)

- [sys.path in Python](https://stackoverflow.com/questions/31291608/effect-of-using-sys-path-insert0-path-and-sys-pathappend-when-loading-modul)

- [Flask documentation home page](https://flask.palletsprojects.com/en/1.1.x/)

- [Flask API docs](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask)

- [flask-peewee docs](https://readthedocs.org/projects/flask-peewee/downloads/pdf/latest/)

- [Implementing API exceptions for Flask](https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/)

- [Discussion on importing from parent dir](https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder)

- [Status codes](https://www.restapitutorial.com/httpstatuscodes.html)

- [Peewee Complex Subquery (Github issue)](https://github.com/coleifer/peewee/issues/1684)

- [Nested aggregates](https://stackoverflow.com/questions/21297971/can-peewee-nest-select-queries-such-that-the-outer-query-selects-on-an-aggregate)

- [Status code for update or delete](https://stackoverflow.com/questions/2342579/http-status-code-for-update-and-delete)

- [Pytest for Flask](https://testdriven.io/blog/flask-pytest/)

- [Making Python packages](https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html)

- [GiveWhenThen](https://martinfowler.com/bliki/GivenWhenThen.html)

- Export ENV variables locally: `export $(egrep -v '^#' env_var | xargs)`

- Ports specified is `external:internal` e.g. `8080:5432` exposes the PostgreSQL container port 5432 to local computer 8080.

- You cannot have:

```yaml
services:
  backend-recipe:
    build: .
      args:
        var: var
```
and only

```
services:
  backend-recipe:
    build:
      context: .
      dockerfile: dockerfile
      args:
        base_path: backend_api
```