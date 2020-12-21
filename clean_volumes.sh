#!/bin/bash

volumes=("pg-volume")

# for e in ${containers[@]}
# do
#     echo "Clearing ${e}"
#     docker ps --filter \
#         "name=${e}" \
#     | grep . \
#     && docker rm "${e}" && echo "Volume removed." \
#     || echo "Container not found."
# done

for e in ${volumes[@]}
do
    echo "VOLUME: Clearing ${e}"
    docker ps --quiet --filter \
        "name=${e}" \
    | grep . \
    | xargs docker rm --force "${e}" \
    && echo "VOLUME: Removed."
done