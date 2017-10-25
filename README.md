This is a prototype for the Cloud Marketplace.

## Quick start

Install Docker, then run:

```
cp .env.sample .env
ln -sf docker-compose.local.yml docker-compose.override.yml
./docker-update.sh
```

Then initialize the database:

```
python manage.py migrate
```

Then start everything up:

```
docker-compose up
```

You can now visit the site at http://localhost:8000/.

## Accessing the main app container

To access the main app container, run:

```
docker-compose run app bash
```

This will run an interactive bash session inside the main app 
container. In this container, the `/cmp` directory is mapped to
the root of the repository on your host.

## A note about manage.py

`manage.py` automatically attempts to run itself inside the app container if
needed, so you can just run it with `python manage.py` on your Docker host.
However, if you run into problems, you can use
`docker-compose run app manage.py` instead.

## Updating the containers

Whenever you update your repository via e.g. `git pull` or
`git checkout`, you should update your containers by running
`./docker-update.sh`.
