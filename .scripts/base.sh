#!/bin/bash

# Functions
function show_help() {
    local TITLE=$1
    echo "Usage: ./run <command>"
    echo "Commands:"

    # Sort command keys
    local sorted_keys=($(for key in "${!COMMANDS[@]}"; do
                echo "$key"
    done | sort))

    # Display sorted commands
    for key in "${sorted_keys[@]}"; do
        echo "  $key"
    done
}

function run_command() {
    local CMD=$1

    if [ -z "$CMD" ]; then
        echo "No command name provided"
        exit 1
    fi

    local SCRIPT=${COMMANDS[$CMD]}
    if [ -z "$SCRIPT" ]; then
        echo "Command not found: $CMD"
        exit 1
    fi

    if [ "$SCRIPT" == "show_help" ]; then
        show_help
    else
        $SCRIPT
    fi
}

# Make sure executed with bash and not sh
if [ -z "$BASH_VERSION" ]; then
    echo "Please run with bash"
    exit 1
fi

# Parse arguments
CMD="$1"
shift
