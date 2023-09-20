FROM tiangolo/uwsgi-nginx:python3.11

WORKDIR /app

COPY requirements.txt ./

RUN apt remove nginx
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

CMD ["uwsgi", "app.ini"]
