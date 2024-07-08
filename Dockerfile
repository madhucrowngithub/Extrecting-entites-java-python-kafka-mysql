FROM python:3.11.7
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /code
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt  --no-cache-dir
RUN python -m spacy download en_core_web_sm
RUN chown 1000:1000 /code
USER 1000:1000
ENV HOME=/code
COPY resources resources
COPY ./my_app_recap/templates templates
COPY dist dist
RUN pip install --force-reinstall dist/*.whl
