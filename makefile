NAME    := hellofresh-takehome
SHELL   := /bin/bash

.PHONY: all clean lint test

setup: set_up_dir
	echo "Setup has finished."

setup_dir:
	source setup.sh

export_keys: $(USER_KEYS)
	echo "Please see README.md on how to export keys in .env file"

build_all: clean_containers clean_volumes
	docker-compose up --build
# 	docker-compose up --build --detached
# 	docker-compose logs --follow

# rm_docker_compose:
# 	docker-compose rm -v --stop --force --file docker-compose.yml

pg_it:
	docker exec -it pg-database bash

rp_it:
	docker exec -it backend-recipe /bin/bash

conn_psql:
	psql --host=localhost \
		--port=8080 \
		--username=user \
		--dbname=hellofresh \
		--password

clean_images:
	bash clear_images.sh

clean_containers:
	bash clear_containers.sh

clean_volumes:
	bash clear_volumes.sh

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