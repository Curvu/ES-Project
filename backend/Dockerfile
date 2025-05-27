FROM python:3.12-slim AS development

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir

COPY . /app

# Alias for python - py
RUN ln -s $(which python3) /usr/bin/py

# Alias for django - python manage.py
RUN echo -e "#!/bin/sh\npython manage.py \$@" > /usr/bin/django && chmod +x /usr/bin/django