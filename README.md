# ElasticTweet
Easily import tweet data into ElasticSearch.


# Runs on my machine with:

Ubuntu 16.04

Python 2.7.12

Virtualenv 15.01


# To install and run the application:

$ chmod +x install.sh

$ ./install.sh

$ chmod +x run.sh

$ ./run.sh


# Alternatively, install using Docker:

$ sudo docker build -t elastictweet:latest .

$ sudo docker run -it --rm --name elastictweet   -v "$PWD":/usr/src/view -w /usr/src/view   -e LANG=C.UTF-8 -e FLASK_APP=view.py --net="host"  -p 5000:5000 elastictweet:


Then open http://127.0.0.1:5000/ in Chrome.

# Using the application

You should arrive at the following landing page.

![Landing page](static/img/landing.png?raw=true "Landing page")


