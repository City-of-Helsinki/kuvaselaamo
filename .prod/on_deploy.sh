#!/bin/bash

#python /app/manage.py migrate --noinput

# Generate the admin user using the password given in the environment variables.
# If no password is set, the admin user gets a generated password which will
# be written in stdout so that it can be accessed during the initial deployment.
#if [[ "$ADMIN_USER_PASSWORD" ]]; then
#    python /app/manage.py add_admin_user -u admin -p $ADMIN_USER_PASSWORD -e admin@example.com
#else
#    python /app/manage.py add_admin_user -u admin -e admin@example.com
#fi

#python /app/manage.py create_initial_page_content

echo "on_deploy.sh here ..."

