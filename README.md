This is a prototype for the Cloud Marketplace.

## Quick start

Install [Docker][], then run:

```
cp .env.sample .env
ln -sf docker-compose.local.yml docker-compose.override.yml
./docker-update.sh
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

## Deploying to cloud environments

The Docker setup can also be used to deploy to cloud environments.

To do this, you'll first need to
[configure Docker Machine for the cloud][docker-machine-cloud],
which involves provisioning a host on a cloud provider and setting up
your local environment to make Docker's command-line tools use that
host. For example, to do this on Amazon EC2, you might use:

```
docker-machine create aws16 --driver=amazonec2
```

Docker Machine's cloud drivers intentionally don't support
folder sharing, which means that you can't just edit a file on
your local system and see the changes instantly on the remote host.
Instead, your app's source code is part of the container image. To
facilitate this, you'll need to create a new Dockerfile that augments
your existing one:

```
cat Dockerfile Dockerfile.cloud-extras > Dockerfile.cloud
```

Also, unlike local development, cloud deploys don't support an
`.env` file. So you'll want to create a custom
`docker-compose.override.yml` file that defines the app's
environment variables, and also points to the alternate Dockerfile:

```
cp docker-compose.cloud.yml docker-compose.override.yml
```

You can edit this file to add or change environment variables as needed.

You'll also want to tell Docker Compose what port to listen on,
which can be done in the terminal by running
`export DOCKER_EXPOSED_PORT=80`.

At this point, you can use Docker's command-line tools and this project's
Docker-related scripts, and your actions will take effect on the remote
host instead of your local machine.

So, you should first run `./docker-update.sh` to set everything up,
followed by `docker-compose up`. Now you should have a server
running in the cloud!

**Note:** A script, [create-aws-instance.sh](./create-aws-instance.sh),
actually automates all of this for you, but it's coupled to Amazon
Web Services (AWS). You're welcome to use it directly or edit it to
your own needs. Run it without any arguments for help.

**Note:** As mentioned earlier, your app's source code is part of
the container image. This means that every time you make a source code
change, you will need to re-run `./docker-update.sh`.

[Docker]: https://www.docker.com/
[docker-machine-cloud]: https://docs.docker.com/machine/get-started-cloud/
