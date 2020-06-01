#!/bin/bash

set -e

if [ -z "$SKIP_DATABASE_CHECK" -o "$SKIP_DATABASE_CHECK" = "0" ]; then
    wait-for-it.sh "${DATABASE_HOST}:${DATABASE_PORT-5432}"
fi


# Apply database migrations
if [[ "$APPLY_MIGRATIONS" = "1" ]]; then
    echo "Applying database migrations..."
    ./manage.py migrate --noinput
fi

# Create admin user. Generate password if there isn't one in the environment variables
if [[ "$CREATE_ADMIN_USER" = "1" ]]; then
    if [[ "$ADMIN_USER_PASSWORD" ]]; then
      PWD=$ADMIN_USER_PASSWORD
    else
      PWD=$(date +%s | sha256sum | base64 | head -c 20)
      echo "Using generated admin user password: $PWD"
    fi

    ./manage.py add_admin_user -u admin -p $PWD -e admin@example.com

    echo "Admin user created with credentials admin (email: admin@example.com)"
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
