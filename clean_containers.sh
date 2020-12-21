#!/bin/bash

containers=("pg-database" "backend-recipe")

# for e in ${containers[@]}
# do
#     echo "Clearing ${e}"
#     docker ps --all --quiet --filter \
#         "name=${e}" \
#     | grep . \
#     && docker stop "${e}" && echo "Container stopped." \
#     && docker rm "${e}" && echo "Container removed." \
#     || echo "Container not found."
# done

for e in ${containers[@]}
do
    echo "CONTAINER: Clearing ${e}"
    docker ps --all --quiet --filter \
        "name=${e}" \
    | grep . \
    | xargs -n 1 docker rm --force \
    && echo "CONTAINER: Removed."
done