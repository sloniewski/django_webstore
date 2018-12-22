FROM python:latest

RUN mkdir /home/project
WORKDIR /home/project
ADD . /home/project
RUN pip install -r requirements.txt

EXPOSE 8000:8000

