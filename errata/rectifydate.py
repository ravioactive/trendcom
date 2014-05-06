from datetime import datetime
import pymongo
import sys

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
db = connection.trendcom
tweets = db.tweets
cursor = tweets.find({}, snapshot = True)
print "total number of tweets found =", cursor.count()
allTweets = [tweet for tweet in cursor]
i, s, p = 0, 100, 10000
for tweet in allTweets:
    datestr = tweet['created_at']
    date = datetime.strptime(datestr, '%a %b %d %H:%M:%S +0000 %Y')
    tweet['timestamp'] = date
    tweets.save(tweet, manipulate = False, safe = True)
    i = i + 1
    if i % s == 0:
        sys.stdout.write(".")
    if i % p == 0:
        print "no problemo in ", i, "tweets!"
