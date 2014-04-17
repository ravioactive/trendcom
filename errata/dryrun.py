import pymongo
import sys
from model import streamfilters
from resources import globalobjs

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string, safe=True)
database = connection.trendcom

crazydump=database.crazydump

def fetchTweets():
    query={}
    selector={}

    try:
        iter=crazydump.find()
    except:
        print "Could not fetch tweet", sys.exc.info()[0]

    #limit=crazydump.count()
    limit=40
    counter=0
    globalobjs.init()

    #print globalobjs.stopwords_list
    for tweetDoc in iter:
        print '\n', counter, '\n', tweetDoc['text'].encode('utf-8','ignore')
        tt=streamfilters.processTweetText(tweetDoc['text'])
        print tt
        counter+=1
        if(counter>=limit):
            break

if __name__ == '__main__':
    fetchTweets()
