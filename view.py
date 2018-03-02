from flask import Flask, render_template, request,json  
from config import *
from elasticsearch import Elasticsearch
import json
import tweepy
import csv


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

# Download tweets using the Tweepy API. The API returns tweets matching the 'query' keyword,
# and number of tweets downloaded equals 'max_tweets'.
def get_tweets(query, max_tweets):
    # Authentication is necessary to interact with the Twitter API through Tweepy.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweets_return = []

    print "Downloading {0} tweets".format(max_tweets)

    i = 1
    # Make use of the Cursor function, that automatically paginates across pages while searching
    # for tweets.
    for tweet in tweepy.Cursor(api.search,
                           q=query,
                           result_type="recent",
                           include_entities=True,
                           lang="en").items():
        
        # Store each tweet's tweet.user.name (twitter name), tweet.user.screen_name (twitter handle),
        # and tweet.text (tweet message).
        tweets_return.append([tweet.user.name, tweet.user.screen_name, tweet.text])
        if i >= int(max_tweets):
        	break
        else:
        	i += 1

    print "Downloaded {0} tweets".format(len(tweets_return))
    return tweets_return


# Pushes tweet data to an ElasticSearch instance.
@app.route('/push_to_es', methods = ['POST'])
def push_to_es():
    print "Pushing tweets to ElasticSearch"
    if request.method == "POST":
        req = json.loads(request.form["tweets"])
        tweets = req["tweets"]

        index = request.form["index"]
        doc_type = request.form["doc_type"]

        es_host = request.form["es_host"]
        es_port = int(request.form["es_port"])

        # Establish a connection with the ElasticSearch instance using a client
        # provided host and port number.
        es = Elasticsearch([{'host': es_host, 'port': es_port}])

        # Push tweets one at a time into the ElasticSearch instance.
        for tweet in tweets:
            es.index(index=index,
            	doc_type=doc_type,
                 body={"name": tweet[0],
                        "screen_name": tweet[1],
                       "message": tweet[2]})

        return json.dumps({'status':'OK'});
    else:
        return json.dumps({'status':'BAD REQUEST'});


# Returns the tweet search history, from a csv file.
@app.route('/history', methods = ['GET'])
def history():
    print "Fetchng search hostory"
    history = []
    with open(r'history/history.csv', 'r') as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            for element in row:
                history.insert(0,element)

    return json.dumps({'status':'OK', "history":history});


# Returns tweets matching a keyword specified by the client.
@app.route('/submit_keyword', methods = ['POST'])
def submit_keyword():
    if request.method == "POST":

        keyword = request.form["keyword"]
        maxTweets = request.form["hmt"]

        # Add this keyword to the search history, stored in a csv file.
        with open(r'history/history.csv', 'a') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([keyword])
        
        query_results = get_tweets(keyword, maxTweets)

        return json.dumps({'status':'OK','tweets':query_results});
    else:
    	return json.dumps({'status':'BAD REQUEST'});