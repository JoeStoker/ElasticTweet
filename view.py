from flask import Flask, render_template, request,json

import json
import tweepy
# FLASK_APP=view.py flask run

# from elasticsearch import Elasticsearch

# import twitter keys and tokens
from config import *

from elasticsearch import Elasticsearch



app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

def get_tweets(query, max_tweets):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweets_return = []
    # searchQuery = '#someHashtag'  # this is what we're searching for
    # maxTweets = 10 # Some arbitrary large number
    tweetsPerQry = 10  # this is the max the API permits
    fName = 'tweets.txt' # We'll store the tweets in a text file.


    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1L

    tweetCount = 0
    print "Downloading max {0} tweets".format(max_tweets)
    
    # while tweetCount < maxTweets:
    #     try:
    #         if (max_id <= 0):
    #             if (not sinceId):
    #                 new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
    #             else:
    #                 new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
    #                                         since_id=sinceId)
    #         else:
    #             if (not sinceId):
    #                 new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
    #                                         max_id=str(max_id - 1))
    #             else:
    #                 new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
    #                                         max_id=str(max_id - 1),
    #                                         since_id=sinceId)
    #         if not new_tweets:
    #             print("No more tweets found")
    #             break
    #         for tweet in new_tweets:
    #             searched_tweets.append([tweet.text, tweet.user.name])
    #         tweetCount += len(new_tweets)
    #         print "Downloaded {0} tweets".format(tweetCount)
    #         max_id = new_tweets[-1].id
    #     except tweepy.TweepError as e:
    #         # Just exit if any error
    #         print("some error : " + str(e))
    #         break
    searched_tweets = []
    # last_id = -1
    # try:
    #     while len(searched_tweets) < max_tweets:
    #         print "looping again, since len(searched_tweets)="+str(len(searched_tweets))+" < max_tweets="+str(max_tweets)
    #         count = int(max_tweets) - len(searched_tweets)
        
    #         print "try to get count="+str(count)+"tweets, since len(searched_tweets="+str(len(searched_tweets))
    #         new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
    #         if not new_tweets:
    #             print "strange error"
    #             break
    #         searched_tweets.extend(new_tweets)
    #         last_id = new_tweets[-1].id
    # except tweepy.TweepError as e:
    #     print "error ", e
    i = 1
    for tweet in tweepy.Cursor(api.search,
                           q=query,
                           result_type="recent",
                           include_entities=True,
                           lang="en").items():
        print "new item! i = "+str(i)
        tweets_return.append([tweet.text, tweet.user.screen_name])
        if i >= int(max_tweets):
        	print"trying to break!"
        	break
        else:
        	i += 1

    # for tweet in searched_tweets:
    # 	tweets_return.append([tweet.text, tweet.user.name])
    print "Downloaded {0} tweets".format(len(tweets_return))
    return tweets_return


@app.route('/push_to_es', methods = ['POST'])
def push_to_es():
    if request.method == "POST":
        print "yay!"
        req = json.loads(request.form["tweets"])
        tweets = req["tweets"]
        index = request.form["index"]
        doc_type = request.form["doc_type"]
        
        print "Index = ",index
        print "Doc_type = ",doc_type
        

        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

        for tweet in tweets:
            print "tweet:",tweet

            es.index(index=index,
            	doc_type=doc_type,
                 body={"screen_name": tweet[1],
                       "message": tweet[0]})

        return json.dumps({'status':'OK'});
    else:
        print "awww"
        return json.dumps({'status':'BAD REQUEST'});

@app.route('/submit_keyword', methods = ['POST'])
def submit_keyword():
   
    if request.method == "POST":
        print "yay!"
        keyword = request.form["keyword"]
        maxTweets = request.form["hmt"]

        
        query_results = get_tweets(keyword, maxTweets)
        return json.dumps({'status':'OK','tweets':query_results});
    else:
    	print "awww"
    	return json.dumps({'status':'BAD REQUEST'});





