NAME    := hellofresh-takehome
SHELL   := /bin/bash

.PHONY: all clean lint test

setup: set_up_dir
	echo "Setup has finished."

setup_dir:
	source setup.sh

export_keys: $(USER_KEYS)
	echo "Please see README.md on how to export keys in .env file"

build_all: clean_all
	docker-compose up --build

build_quick: clean_containers clean_volumes
	docker-compose up

pg_it:
	docker exec -it pg-database bash

rp_it:
	docker exec -it backend-recipe /bin/bash

conn_psql:
	psql --dbname=hellofresh \
		--host=localhost \
		--port=8080 \
		--username=user \
		--password

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