#!/bin/bash

set -e

echo "docker-entrypoint.sh here ..."

if [ -z "$SKIP_DATABASE_CHECK" -o "$SKIP_DATABASE_CHECK" = "0" ]; then
    until nc -z -v -w30 "${DATABASE_HOST}" "${DATABASE_PORT-5432}"
    do
        echo "Waiting for postgres database connection..."
        sleep 1
    done
    echo "Database is up!"
fi


# Apply database migrations
if [[ "$APPLY_MIGRATIONS" = "1" ]]; then
    echo "Applying database migrations..."
    ./manage.py migrate --noinput
fi

# Create admin user. Generate password if there isn't one in the environment variables
if [[ "$CREATE_ADMIN_USER" = "1" ]]; then
    if [[ "$ADMIN_USER_PASSWORD" ]]; then
      ./manage.py add_admin_user -u kuva-admin -p $ADMIN_USER_PASSWORD -e kuva-admin@hel.ninja
    else
      ./manage.py add_admin_user -u kuva-admin -e kuva-admin@hel.ninja
    fi
fi

# Apply database migrations
if [[ "$ADD_INITIAL_CONTENT" = "1" ]]; then
    echo "Adding initial content..."
    ./manage.py create_initial_page_content
fi

# Start server
if [[ ! -z "$@" ]]; then
    "$@"
elif [[ "$DEV_SERVER" = "1" ]]; then
    python ./manage.py runserver 0.0.0.0:8080
else
    uwsgi --ini .prod/uwsgi.ini
fi

echo "docker-entrypoint.sh here ... done"