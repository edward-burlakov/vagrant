FROM python:3-alpine

WORKDIR /code

COPY requirements.txt  /code
RUN  mkdir db
RUN pip install -r requirements.txt

COPY . /code

EXPOSE  8000

VOLUME ["django-base"]

CMD  sh init.sh  && python3 manage.py runserver 0.0.0.0:8000   