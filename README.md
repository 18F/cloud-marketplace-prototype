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

To access the main app container, run:

```
docker-compose run app bash
```

This will run an interactive bash session inside the main app 
container. In this container, the `/cmp` directory is mapped to
the root of the repository on your host.

## Updating the containers

Whenever you update your repository via e.g. `git pull` or
`git checkout`, you should update your containers by running
`./docker-update.sh`.
