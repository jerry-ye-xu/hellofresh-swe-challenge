#!/bin/bash

set -e

until PGPASSWORD=${POSTGRES_PASSWORD} psql  \
    --username="${POSTGRES_USER}" \
    --dbname="${POSTGRES_DB}" \
    --host="${POSTGRES_HOST_FROM_BACKEND}" \
    --port="${POSTGRES_PORT}" \
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