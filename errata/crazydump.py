import sys
import tweepy
import json
import pymongo

consumer_key=""
consumer_secret=""
access_key = ""
access_secret = ""
x_consumer_key = "cYyGL0vbIRWMiTAJ9rcQ8A"
x_consumer_secret = "HVWH8oe5ut6hpoD5HbkKVtBU0StYuBVezbg0iIHklpc"
x_access_token = "51518286-uSn7aIdVPSfQBk6uWexPqdU8cx6SPTMrNLvlo1tpC"
x_access_token_secret = "e2AKBACbYgUvaVZOcAnv5wlxEKjsl3wfR1PfE7uXLuvFt"

connection = pymongo.Connection("mongodb://localhost", safe=True)

db = connection.trendcom
dump = db.crazydump

auth = tweepy.OAuthHandler(x_consumer_key, x_consumer_secret)
auth.set_access_token(x_access_token, x_access_token_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text

    def on_data(self, tweet):
        jsontweet = json.loads(tweet)
        dump.insert(jsontweet)
        print jsontweet

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(track=['bebo'])

