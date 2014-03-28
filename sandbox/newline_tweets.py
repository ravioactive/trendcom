import tweepy
from tweepy.parsers import Parser
import json

x_consumer_key = "cYyGL0vbIRWMiTAJ9rcQ8A"
x_consumer_secret = "HVWH8oe5ut6hpoD5HbkKVtBU0StYuBVezbg0iIHklpc"
x_access_token = "51518286-uSn7aIdVPSfQBk6uWexPqdU8cx6SPTMrNLvlo1tpC"
x_access_token_secret = "e2AKBACbYgUvaVZOcAnv5wlxEKjsl3wfR1PfE7uXLuvFt"

auth = tweepy.OAuthHandler(x_consumer_key, x_consumer_secret)
auth.set_access_token(x_access_token, x_access_token_secret)

class RawJsonParser(Parser):
    def parse(self, method, payload):
        return payload

api = tweepy.API(auth_handler=auth, parser=RawJsonParser())
mytweets=api.user_timeline()
jsonmytweets=json.loads(mytweets)
#print jsonmytweets
for item in jsonmytweets:
    print item, '\n'
    break
#print mytweets
#for tweet in mytweets:
#    print tweet
