
import streamfilters
import pymongo
import json
#import logger - logging suppport

def insertMongo(twitterResponseJSON, trendId, db):
    print "Adding tweet for trend:", trendid
    #TODO: logRaw(twitterResponseJSON)
#    logactivity() -- Idea is to have one central log of everything
    tweetJSON = json.loads(twitterResponseJSON)
    ret = addTweet(tweetJSON, trendId, db)
    ret += addUser(tweetJSON, trendId, db)
    return ret

def addTweet(tweetJSON, trendId, db):
    tweet = fetchTweet(tweetJSON, trendId, db)
    #if(tweetDNE(tweenJSON, db)):
    if tweet is None:
        newtweet = parseTweet(tweetJSON)
        pushTrendInto(newtweet,trendId) #this is a list-correct this.
        tweets = db.tweets
        tweets.insert(newtweet)
        print "Adding tweet for trend:", trendId
        #TODO: logtweet(newtweet)
        return newtweet['text']
    else:
        #tweetReady = fetchTweet(tweetJSON, trendId, db)
        #Add log for fetchedTweet in fetchTweet
        pushTrendInto(tweet,trendId)
        return tweet['text']

def addUser(tweetJSON, trendId, db):
    user = fetchUser(tweetJSON, trendId, db)
    if user is None:
        newuser = parseUser(tweetJSON)
        pushTrendInto(newuser,trendId)
        users = db.users
        users.insert(newuser)
        print "Adding user for trend", trendId
        #TODO: loguser(newuser)
        return newuser['name']
    else:
        #userReady = fetchUser(tweetJSON, trendId, db)
        # loguser({"user":userReady['id'],"alreadyExists":"true"}) --should go in fetchUser
        pushTrendInto(user,trendId)
        return user['name']

def addTrend(trend, db):
    trend=fetchTrend(trend,db)
    if trend is None:
        print "Adding trend"
        trends = db.trends
        trendId = trends.count() + 1        #How to find auto incrementing id?
        newtrend = {"_id":trend,"trendId":trendId}
        trends.insert(newtrend)
        #TODO: logtrend(newtrend)
        return trendId
    else:
        #trend = fetchTrend(trend, db)
        # log trend re-fetched in fetchTrend?
        return trend.trendId
    #find trend if already exists
    #return trend

################################## TREND OPS ##################################

def fetchTrend(trend, db):
    #log refetching
    trends=db.trends
    t=trends.find_one({'_id':trend});
    return t

def pushTrendInto(jsonModel,trendId):
    trends=jsonModel['trends']
    if trends is None:
        trends=[]
    elif trendId not in trends:
        trends.append(trendId)

#Unused
def seenForTrend(jsonModel,trendId):
    trends=jsonModel['trends']
    if trends is None:
        return False
    else:
        return trendId in trends

################################## TWEET OPS ##################################
# Tweet obj:
#     * user_id
#     * text
#     * id_str
#     * lang
#     * geo,coordinates,place
#     * created_at
#     * trend_id

def parseTweet(tweetJSON):
    #TODO
    parsedTweet = {};
    tweet_text=tweetJSON['text']
    parsedTweet['text'] = tweet_text

    tokenizedTweet=processTweetText(tweet_text)
    parsedTweet['tokens']=tokenizedTweet

    parsedTweet['_id'] = tweetJSON['id_str']
    parsedTweet['lang'] = tweetJSON['lang']
    if tweetJSON['geo'] == "":
        parsedTweet['loc'] = tweetJSON['user']['location']
    else:
        parsedTweet['loc'] = tweetJSON['geo']
    parsedTweet['created_at'] = tweetJSON['created_at']
    return parsedTweet

def fetchTweet(tweetJSON, trendId, db):
    # log refetching
    tweetId = tweetJSON['id_str']
    tweets=db.tweets
    tweet = tweets.find_one({'_id':tweetId})
    return tweet

################################## USER OPS ##################################
# User obj:
#     * id_str
#     * location
#     * name
#     * screen_name
#     * trend_ids []

def parseUser(tweetJSON):
    parsedUser = {}
    parsedUser['_id']=tweetJSON['user']['id']
    parsedUser['loc']=tweetJSON['user']['location']
    parsedUser['name']=tweetJSON['user']['name']
    parsedUser['handle']=tweetJSON['user']['screen_name']
    return parsedUser

def fetchUser(tweetJSON, trendId, db):
    # log refetching
    userId=tweetJSON['user']['id']
    users=db.users
    user = users.find_one({'_id':userId})
    return user


#===deprecated===
# def trendDNE(trend, db):
#     #separated to be implemeted as fast as possible
#     return False

# def tweetDNE(tweetJSON, db):
#     #separated to be implemeted as fast as possible
#     tweetId = tweetJSON['id_str']
#     tweets=db.tweets
#     tweet = tweets.find_one({'_id':tweetId})
#     if(tweet==null):
#         return False
#     else:
#         return True

# def userDNE(tweetJSON, db):
#     #separated to be implemeted as fast as possible
#     userId=tweetJSON['user']['id']
#     users=db.users
#     user = users.find_one({'_id':userId})
#     if(user==null):
#         return False
#     else:
#         return True
