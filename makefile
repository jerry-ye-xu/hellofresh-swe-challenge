NAME    := hellofresh-takehome
SHELL   := /bin/bash
VERSION := $(shell cat VERSION)

export_keys: $(USER_KEYS)
	echo "Please see README.md on how to export keys in env_var_local file"

build_all: clean_all
	docker-compose up --build

build_quick: prune_images clean_containers clean_volumes
	docker-compose build
	docker-compose up

# build_all

run_tests:
	newman run ./postman_tests/HF-dimensions.postman_collection.json
	newman run ./postman_tests/HF-ratings.postman_collection.json
	newman run ./postman_tests/HF-recipes.postman_collection.json
	newman run ./postman_tests/HF-weekly-meals.postman_collection.json

pg_it:
	docker exec -it pg-database bash

rp_it:
	docker exec -it backend-recipe /bin/bash

conn_psql:
	psql --dbname=${POSTGRES_DB} \
		--host=${POSTGRES_HOST} \
		--port=${POSTGRES_PORT} \
		--username=${POSTGRES_USER} \
		--password

prune_images:
	docker image prune --force

clean_images:
	bash clean_images.sh

clean_containers:
	bash clean_containers.sh

clean_volumes:
	bash clean_volumes.sh

clean_all: clean_containers clean_volumes clean_images

# test:
# 	docker ps --all --quiet --filter \
# 		"name=pg-database" \
# 	| grep . \
# 	&& docker stop "pg-database" \
# 	&& docker rm "pg-database" \
# 	&& docker rmi "pg-database"

# 	docker images --all --quiet --filter "reference=*backend-recipe" \
# 	| grep . \
# 	 docker image rm .

# 	 docker rmi $(shell docker images --all --quiet --filter "reference=*backend-recipe" | uniq)