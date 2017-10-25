FROM python:3.6.2

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -

# Note that we want postgresql-client so 'manage.py dbshell' works.
RUN apt-get update && \
  apt-get install -y nodejs postgresql-client

RUN pip install virtualenv

WORKDIR /cmp

RUN npm install -g yarn

ENV PATH /cmp/node_modules/.bin:$PATH
ENV DDM_IS_RUNNING_IN_DOCKER yup

ENTRYPOINT ["python", "/cmp/docker_django_management.py"]
