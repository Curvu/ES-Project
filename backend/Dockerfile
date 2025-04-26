FROM python:3.12-slim AS development

RUN apk update && apk add --no-cache \
  build-base

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir

COPY . /app

# Alias for python - py
RUN ln -s $(which python) /usr/bin/py

# Alias for django - python manage.py
RUN echo -e "#!/bin/sh\npython manage.py \$@" > /usr/bin/django && chmod +x /usr/bin/django