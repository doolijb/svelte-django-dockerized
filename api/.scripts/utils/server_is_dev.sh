#! bash
# Make sure SERVER_TYPE=dev
if [ ! $SERVER_TYPE = "DEV" ]; then
    echo "ERROR: Only execute this script in a dev environment!"
    echo "Expected: SERVER_TYPE=DEV"
    echo "Received: SERVER_TYPE=$SERVER_TYPE"
    exit 1
fi