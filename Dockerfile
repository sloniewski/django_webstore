FROM python:latest

RUN pip install --upgrade pip
RUN mkdir /home/project && cd /home/project && git clone https://github.com/sloniewski/django_webstore.git
RUN pip install -r /home/project/django_webstore/requirements.txt

RUN apt-get update
RUN apt-get install -y postgresql postgresql-contrib
USER postgres
RUN  /etc/init.d/postgresql start &&\
    psql --command "CREATE USER db_user WITH SUPERUSER PASSWORD 'super_secret';" &&\
       createdb -O db_user webstore

# /etc/init.d/postgresql restart
CMD ./home/project/django_webstore/manage.py migrate

EXPOSE 8000:8000