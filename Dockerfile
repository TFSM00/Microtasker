FROM python:3.12.0rc3-alpine3.18

WORKDIR /app

COPY requirements.txt ./

RUN apk add linux-headers
RUN apk add build-base
RUN pip install -r requirements.txt

COPY . /app

CMD ["uwsgi", "app.ini"]
