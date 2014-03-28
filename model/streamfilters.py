# -*- coding: utf-8 -*-

import re
from collections import defaultdict
import sys
import os
from unidecode import unidecode

#===============ENCODE===============
def encodeStream(tweet):
    #tweet=unicode(tweet,'utf-8')
    #tweet=tweet.encode('utf-8','ignore')
    tweet=unidecode(tweet)
    tweet=tweet.lower()
    return tweet


#===============CLEANSING===============
def removeUrl(tweet):
    urlpat=re.compile(r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
    tweet = re.sub(urlpat, '', tweet)
    return tweet

def removeMentions(tweet):
    tweet = re.sub('@[^\s]+','',tweet)
    return tweet

def removeHashtags(tweet):
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    return tweet


#===============TRIMMING===============
def removeMetaPunct(tweet):
    tweet=re.sub('[^a-zA-Z0-9]+',' ',tweet)
    return tweet

def replaceRepeats_gt2(tweet_tokens):
    replacedTokens=[]
    pat = re.compile(r"(.)\1{2,}", re.DOTALL)
    subspat = r"\1\1"
    for token in tweet_tokens:
        replacedTokens.append(re.sub(pat, subspat, token))
    return replacedTokens

def trimTweet(tweet):
    return tweet.strip()


#===============TOKENIZATION===============
def tokenizeTweet(tweet):
    return [t for t in tweet.split(' ') if t is not '']


#===============STOPWORDS===============
def getAllStopwords():
    allStopWordsFile=os.path.join(os.path.join(os.path.join(os.path.join(os.path.abspath(os.path.pardir),''),'resources'),'stopwords'),'all_stopwords.txt')
    return open(allStopWordsFile,'r').read().splitlines()

def removeStopWords(tweet_tokens):
    stopwords_list=getAllStopwords()
    after_stopwords=[tok for tok in tweet_tokens if tok not in stopwords_list]
    return after_stopwords


#===============SLANGS===============
def getSlangDictionary():
    allSlangWordsFile=os.path.join(os.path.join(os.path.join(os.path.join(os.path.abspath(os.path.pardir),'code'),'resources'),'slangwords'),'all_slangwords.txt')
    return {k:v for (k,v) in [slw.split(':') for slw in open(allSlangWordsFile,'r')]}

def translateSlangs(tweet_tokens):
    slangDict=getSlangDictionary()
    return [subel for sub in [slangDict[tok].split() if tok in slangDict and slangDict[tok] is not '' else [tok] for tok in tweet_tokens] for subel in sub]


#===============BINDER FUNCTION===============
#   [Y]encode -> [Y]trim -> [Y]urls -> [Y]mentions -> [Y]hashtags ->
#                [Y]punctuation -> [Y]metachar -> [Y]trim ->
#   [Y]tokenize ->
#                [N]slangs -> [Y]replaceGT2 -> [N]slangs -> [Y]stopwords

def processTweetText(tweet):
#   [Y]encode ->
    tweet=encodeStream(tweet)


#   [Y]trim ->
    tweet=trimTweet(tweet)
#   [Y]urls->
    tweet=removeUrl(tweet)
#   [Y]mentions
    tweet=removeMentions(tweet)
#   [Y]hashtags ->
    tweet=removeHashtags(tweet)


#   [Y]punctuation -> [Y]metachar ->
    tweet=removeMetaPunct(tweet)
#   [Y]trim ->
    tweet=trimTweet(tweet)


#   [Y]tokenize->
    tokens=tokenizeTweet(tweet)


#   [N]slangs->
    tokens=translateSlangs(tokens)
#   [Y]repeats->
    tokens=replaceRepeats_gt2(tokens)
#   [N]slangs->
    tokens=translateSlangs(tokens)
#   [Y]stopwords->
    tokens=removeStopWords(tokens)

    return tokens


def testTweetProcessor():
    #Works!
    url_test=["Office For iPhone And Android Is Now Free  http://tcrn.ch/1rH7Fkx  by @alex",
    "1. amazing fit  @TBdressClub dress=>http://goo.gl/qwIwus        shoes=>http://goo.gl/Y95sdJ   pic.twitter.com/3dE4SFgUmT"]
    for urls in url_test:
        print 'removeUrl BEFORE:', urls
        print 'removeUrl AFTER:', removeUrl(urls)

    #works!
    mention_test=u"Like our @FInishLine images for #MarchMadness? Here they are. Even the ones that didn't make the cut. http://blog.finishline.com/2014/03/24/rep-your-team-for-march-madness/ …".encode('utf-8','ignore')
    print 'removeMentions BEFORE:', mention_test
    print 'removeMentions AFTER:', removeMentions(mention_test)

    #works!
    hashtag_test="Top shares this week! The latest on #MarchMadness and this year's #Sweet16 and Obama's plan inRussia and Crimea http://shar.es/B32pX "
    print 'removeHashtags BEFORE:', hashtag_test
    print 'removeHashtags AFTER:', removeHashtags(hashtag_test)

    #works!
    whitespace_test="    The @SEC was\n\n    7th in Conference RPI during the regular season. They’re 7-0 in the NCAA Tournament. #MarchMadness   "
    #whitespace_test="new\nline\ntwee..\n\n..eet"
    print 'remove white space BEFORE:', whitespace_test
    print 'remove white space AFTER:', trimTweet(removeMetaPunct(whitespace_test))

    #DONE
    metachar_test="new\nline\ntwee..\n\n..eet"
    print 'removeMetachars BEFORE:', metachar_test
    print 'removeMetachars AFTER:', removeMetaPunct(metachar_test)

    #Doesn't work
    punctuation_meta_test="Ohhh Shittt...it's missed gym o'clock again...FUCK!!\n*cracks 3rd beer"
    print 'removeMetaPunct BEFORE:', punctuation_meta_test
    print 'removeMetaPunct AFTER:', removeMetaPunct(punctuation_meta_test)

    #Doesn't work
    repeats_test="Ohhh Shittt it's missed gym o'clock again...FUCKKKK!!\n*cracks 3rd beer"
    print 'replaceRepeats_gt2 BEFORE:', repeats_test
    print 'replaceRepeats_gt2 AFTER:', replaceRepeats_gt2(repeats_test.split())

    #works!
    stopword_test='anybody considering best inward several provided'
    stopword_test_tokens=stopword_test.split()
    print 'removeStopWords BEFORE:', stopword_test_tokens
    print 'removeStopWords AFTER:', removeStopWords(stopword_test_tokens)

    #slangword_test=''

if __name__ == '__main__':
    testTweetProcessor()
