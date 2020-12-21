#!/bin/bash

set -e

until PGPASSWORD=${POSTGRES_PASSWORD} psql  \
    --dbname="${POSTGRES_DATABASE}" \
    --host="${POSTGRES_HOST}" \
    --port="${POSTGRES_PORT}" \
    --username="${POSTGRES_USER}" \
    -c '\q';
do
    echo "Postgres is unavailable - sleeping"
    sleep 1
done

echo "Postgres is up - executing command"

echo "Running create_schemas.py"
python3 ./src/db_setup/create_schemas.py
echo "Running create_tables.py"
python3 ./src/db_setup/create_tables.py
echo "Running populate_tables.py"
python3 ./src/db_setup/populate_tables.py