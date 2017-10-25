#! /bin/sh

set -e

echo "----- Updating Python Dependencies -----"
python -m pip install -r requirements-dev.txt

echo "----- Updating Node Dependencies -----"
yarn

# Note that much of the following will eventually be uncommented.

#echo "----- Migrating Database -----"
#python manage.py migrate --noinput

#echo "----- Initializing Groups -----"
#python manage.py initgroups

#if [ -n "${APP_IS_ON_DOCKER_IN_CLOUD}" ]; then
#  echo "----- Building Static Assets -----"
#  gulp build
#fi
