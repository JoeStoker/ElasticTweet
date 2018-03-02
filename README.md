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

# Tutorial - Using the application

You should arrive at the following landing page. Press on the "use app" button to procede.

![Landing page](static/img/landing.png?raw=true "Landing page")

You may type in any Keyword, specifying tweets to search for. Specify the number of tweets. 

![Keywords](static/img/keyword.png?raw=true "Keyword")

By pressing "Get tweets", the specified number of tweets are returned. Pressing "History" displays the search history.

![Results](static/img/results.png?raw=true "Results")

Pressing the "x" button next to the "Results" heading clears the results table.

One can now specify ElasticSearch and Kibana configuration details.

![Configuration](static/img/configurations.png?raw=true "Configuration")

After searching for tweets and specifying configuration details, one can push the search results to ElasticSearch. An index and doc_type should be specified. The tweets can then be viewed and analysed in Kibana.

![Push](static/img/push.png?raw=true "Push")


