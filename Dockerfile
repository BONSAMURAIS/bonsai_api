FROM python:3-alpine 

LABEL Description="This image holds a flask app for bonsai api" Version="0.1.0"

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

RUN pip install gunicorn
RUN pip install -e .
ENTRYPOINT gunicorn -b :5000 bonsai_api:"create_app()"
