#! bash

# If --silent flag is passed, then we will not print the output
if [[ "$1" == "--silent" ]]; then
    SILENT="> /dev/null 2>&1"
fi

eval $"$DOCKER_COMPOSE down $SILENT"
