# -*- coding: utf-8 -*-
import tweepy
import sys
import os
from model import mongomodel
from resources import globals

class MongoStreamListener(tweepy.StreamListener):
    def __init__(self, trend, db, logfile):
        self.trend = trend
        self.db = db
        self.trendId = mongomodel.addTrend(trend, db)
        self.logfile = logfile
        self.calls = 0
        self.step = 1000
        self.smallstep = 100

    def on_status(self, status):
        #print status.text
        pass

    def on_data(self, tweet):
        #DAO based approach, initdao in __init__?
        self.calls += 1
        ret = mongomodel.insertMongo(tweet, self.trendId, self.db)
        ret = ret.encode('utf-8','ignore')
        self.logfile.write(ret)
        if self.calls%self.step == 0:
            print globals.getUptime(), 'taken for', self.calls, 'tweets'
        if self.calls%self.smallstep == 0:
            sys.stdout.write('.')
        #print "RET:\n", ret

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

def main():
    globals.init()
    consumer_key = globals.x_consumer_key
    consumer_secret = globals.x_consumer_secret
    access_token = globals.x_access_token
    access_token_secret = globals.x_access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    args = sys.argv[1:]

    if len(args)<1:
        print "Tweet collections USAGE: missing \'trend\' argument"
        sys.exit(1)

    trend = sys.argv[1]
    if not trend or trend =='':
        print "Value for argument \'trend\' is either blank or d.n.e."
        sys.exit(1)

    print "Tweet collection for trend ", trend, '...'

    sapi = tweepy.streaming.Stream(auth, MongoStreamListener(trend, globals.db, globals.logfile))
    sapi.filter(track=[trend])
    globals.destroy()

if __name__ == '__main__':
    main()
