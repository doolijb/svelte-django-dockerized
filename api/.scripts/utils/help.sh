#! bash
# List all scripts
echo "Help for API scripts:"
echo "  Usage: ./scripts/run <command> [flags] [args]"
echo "  Example: ./scripts/run serve"
echo "  Flags:"
echo "    -  --detach --silent  |Runs command in background, no output"
echo "  Primary API commands:"
# List all scripts in ./scripts/run
for script in \
    "serve              |Runs Django development server i.e 'python manage.py runserver 0.0.0.0:8080'" \
    "migrate            |Runs Django database migrations i.e 'python manage.py migrate'" \
    "shell              |Runs Django shell i.e 'python manage.py shell'" \
    "test               |Runs Django tests i.e 'python manage.py test'" \
    "cmd                |Runs Django management command i.e 'python manage.py <command>'" \
    ; do
    echo "    -  $script"
done

echo "  Additional command scripts:"
# List all scripts in .scripts except for ./run and ./utils
for file in .scripts/*; do
    if [ -d $file ]; then
        for subfile in $file/*; do
            if [ -f $subfile ] && [ $(basename $file) != "utils" ]; then
                echo "    -  $(basename $file):$(basename $subfile)"
            fi
        done
    else
        if [ -f $file ] && [ $(basename $file) != "run" ]; then
            echo "    -  $(basename $file)"
        fi
    fi
done
exit 0