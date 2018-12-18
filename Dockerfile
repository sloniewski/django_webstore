FROM python:latest

RUN pip install --upgrade pip
RUN mkdir /home/project && cd /home/project && git clone https://github.com/sloniewski/django_webstore.git
RUN pip install -r /home/project/django_webstore/requirements.txt

EXPOSE 8000:8000