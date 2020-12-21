#!/bin/basH

docker images --all --quiet --filter "reference=*backend-recipe" \
    | grep . \
    | xargs docker rmi \
    && echo "IMAGE: Removed."

# docker rmi -f $(docker images --filter "dangling=true" --quiet)