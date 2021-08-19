FROM ubuntu:latest
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN apt-get -y update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install libmysqlclient-dev -y
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
COPY . /code/

EXPOSE 8000

CMD exec gunicorn iplseason.wsgi:application --bind 0.0.0.0:8000 --workers 3 
