FROM python:3.4-stretch

RUN mkdir /home/project
WORKDIR /home/project
ADD requirements.txt /home/project/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000:8000

