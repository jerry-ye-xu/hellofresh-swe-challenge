#!/bin/bash

#!/bin/bash

images=("backend-recipe" "postgres")

for e in ${images[@]}
do
    echo "IMAGE: Clearing ${e}"
    docker images --all --quiet --filter "reference=*${e}*" \
        | grep . \
        | xargs docker rmi \
        && echo "IMAGE: Removed."
done

# docker images --all --quiet --filter "reference=*backend-recipe" \
#     | grep . \
#     | xargs docker rmi \
#     && echo "IMAGE: Removed."

# docker rmi -f $(docker images --filter "dangling=true" --quiet)