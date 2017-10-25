#! /bin/sh

set -e

echo "----- Updating Python Dependencies -----"
python -m pip install -r requirements-dev.txt

echo "----- Updating Node Dependencies -----"
yarn

echo "----- Migrating Database -----"
python manage.py migrate --noinput

#if [ -n "${APP_IS_ON_DOCKER_IN_CLOUD}" ]; then
#  echo "----- Building Static Assets -----"
#  gulp build
#fi
