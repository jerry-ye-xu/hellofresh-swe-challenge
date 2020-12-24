import os

from flask import current_app, g
from flask.cli import with_appcontext

from peewee import PostgresqlDatabase

def get_db():
    if 'db' not in g:
        psql_db = PostgresqlDatabase(
            database=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host=os.environ['POSTGRES_HOST_FROM_BACKEND_LOCAL'],
            port=os.environ['POSTGRES_PORT']
        )
        g.db = psql_db.connect()

        return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

def init_app(app):
    app.teardown_appcontext(close_db)