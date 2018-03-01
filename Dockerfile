FROM ubuntu:latest
MAINTAINER Joe Stoekr "jmstoker95@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y virtualenv
COPY . /app
WORKDIR /app
RUN rm -rf flask
RUN virtualenv --python=/usr/bin/python2.7 flask
RUN . flask/bin/activate
RUN pip install -r requirements.txt
EXPOSE 5000
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]