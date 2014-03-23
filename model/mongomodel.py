
import streamfilters
import pymongo
import json
import logger

def insertMongo(twitterResponseJSON, trendId, db):
    print "Adding tweet for trend:", trendid
    logRaw(twitterResponseJSON)
#    logactivity() -- Idea is to have one central log of everything
    tweetJSON = json.loads(twitterResponseJSON)
    ret = addTweet(tweetJSON, trendId, db)
    ret += addUser(tweetJSON, trendId, db)
    return ret

def addTweet(tweetJSON, trendId, db):
    if(tweetDNE(tweenJSON, db)):
        tweetReady = parseTweet(tweetJSON)
        tweets = db.tweets
        tweets.insert(tweetReady)
        print "Adding tweet for trend:", trendId
        logtweet(tweetReady)
        return tweetReady['str']
    else:
        tweetReady = fetchTweet(tweetJSON, trendId, db)
        #Add log for fetchedTweet in fetchTweet
        return tweetReady['str']

def addUser(tweetJSON, trendId, db):
    if(userDNE(tweetJSON, db)):
        userReady = parseUser(tweetJSON)
        users = db.users
        users.insert(userReady)
        print "Adding user for trend", trendId
        loguser(userReady)
        return userReady['name']
    else:
        userReady = fetchUser(tweetJSON, trendId, db)
        # loguser({"user":userReady['id'],"alreadyExists":"true"}) --should go in fetchUser
        return userReady['name']

def addTrend(trend, db):
    if(trendDNE(trend, db)):
        print "Adding trend"
        trends = db.trends
        #How to find auto incrementing id?
        trendId = trends.count() + 1
        trend = {"_id":trend,"trendId":trendId}
        trends.insert(trend)
        logtrend(trend)
        return trendId
    else:
        trend = fetchTrend(trend, db)
        # log trend re-fetched in fetchTrend?
        return trend.trendId
    #find trend if already exists
    return trend

# TWEET OPS

def parseTweet(tweetJSON):
    #TODO
    return parsedTweet

def tweetDNE(tweetJSON, db):
    #separated to be implemeted as fast as possible
    return False

def fetchTweet(tweetJSON, trendId, db):
    # log refetching
    return tweet

# USER OPS

def parseUser(tweetJSON):
    return parsedUser

def userDNE(tweetJSON, db):
    #separated to be implemeted as fast as possible
    return False

def fetchUser(tweetJSON, trendId, db):
    # log refetching
    return user

# TREND OPS

def trendDNE(trend, db):
    #separated to be implemeted as fast as possible
    return False

def fetchTrend(trend, db):
    #log refetching
    return trend
