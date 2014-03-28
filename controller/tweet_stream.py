import tweepy
import sys
import json
import mongomodel
import pymongo

x_consumer_key = "cYyGL0vbIRWMiTAJ9rcQ8A"
x_consumer_secret = "HVWH8oe5ut6hpoD5HbkKVtBU0StYuBVezbg0iIHklpc"
x_access_token = "51518286-uSn7aIdVPSfQBk6uWexPqdU8cx6SPTMrNLvlo1tpC"
x_access_token_secret = "e2AKBACbYgUvaVZOcAnv5wlxEKjsl3wfR1PfE7uXLuvFt"

t_consumer_key = "wgCW9kuShXD8Ck9oPibLhw"
t_consumer_secret = "YK7dvpmpXvqkEtzBPD2R3cpWZOPgtiFtAlg3uifHU"
t_access_token = "51518286-kVybQaBS0hKzcJaZA5fVk39bHTnMkqVeXuyF2qvUB"
t_access_token_secret = "H8RNy01CpIEcBhn9wqTek2YEOjYtaVkiYirirK2s6YBCl"

class MongoStreamListener(tweepy.StreamListener):
    # def __init__(self, tweetDAO, userDAO):
    #     self.tweetDAO = tweetDAO
    #     self.userDAO = userDAO

    def __init__:(self, trend, db):
        self.trend = trend
        self.db = db
        self.trendId = addTrend(trend, db)

    def on_status(self, status):
        print status.text

    def on_data(self, tweet):
        # tweetRet = tweetDAO.addTweet(tweet)
        # userRet = userDAO.addUser(tweet)

        # tweetStr = addTweet(tweet, trendId, db)
        # userStr = addUser(tweet, trendId, db)
        # print userStr, ":", tweetStr

        ret = insertMongo(tweet, trendId, db)
        print ret

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

def main():
    consumer_key = x_consumer_key
    consumer_secret = x_consumer_secret
    access_token = x_access_token
    access_token_secret = x_access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    database = connection.trendcom

    # tweetDB = tweetDAO.starter(database)
    # userDB = userDAO.starter(database)

    # sapi = tweepy.streaming.Stream(auth, MongoStreamListener(tweetDB,userDB))

    trend = ''
    sapi = tweepy.streaming.Stream(auth, MongoStreamListener(trend, db))
    sapi.filter(track=[trend])

#__name__='__tweet_stream__'

if __name__ == '__main__':
    main()

# def getMongoDB(conn_str):
#     connection_string = "mongo://localhost"
#     connection = pymongo.MongoClient(connection_string)
#     database = connection.trendcom
#     return database

# def streamBegin(auth, mongoSL):
#     sapi = tweepy.streaming.Stream(auth, mongoSL)
#     sapi.filter(track=['bebo'])


# def main():

#     tweetDB = tweetDAO.starter(database)
#     userDB = userDAO.starter(database)





# if __name__ == '__main__':
#   main()
