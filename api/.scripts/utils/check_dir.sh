#! bash
if [ ! -d "/srv/www/api" ]; then
    echo "ERROR: Executed from unsafe directory!"
    echo "Expected: /srv/www/api"
    echo $"Received: $(pwd)"
    exit 1
fi