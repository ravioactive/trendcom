# -*- coding: utf-8 -*-

import re
from collections import defaultdict
import sys
import os
from unidecode import unidecode

    # tweet = tweet.lower()
    # #Convert www.* or https?://* to URL
    # tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
    # #Convert @username to AT_USER
    # tweet = re.sub('@[^\s]+','AT_USER',tweet)
    # #Remove additional white spaces
    # tweet = re.sub('[\s]+', ' ', tweet)
    # #Replace #word with word
    # tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # #trim
    # tweet = tweet.strip('\'"')

#===============ENCODE===============
def encodeStream(tweet):
    #tweet=unicode(tweet,'utf-8')
    #tweet=tweet.encode('utf-8','ignore')
    tweet=unidecode(tweet)
    tweet=tweet.lower()
    return tweet


#===============CLEANSING===============
def removeUrl(tweet):
    tweet=re.sub('((www\.[\s]+)|(https?://[^\s]+))','',tweet)
    return tweet

def removeMentions(tweet):
    tweet = re.sub('@[^\s]+','',tweet)
    return tweet

def removeHashtags(tweet):
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    return tweet


#===============TRIMMING===============
def removeWhitespace(tweet):
    tweet = re.sub('[\s]+', ' ', tweet)
    return tweet

def removePunctuation(tweet):
    tweet=tweet.strip('\'"')
    tweet=tweet.strip('\'"?,.')
    tweet=tweet.strip('/')
    return tweet

def replaceRepeats_gt2(tweet_tokens):
    pattern=re.compile(r"(.)\1{1,}", re.DOTALL)
    for t in tweet_tokens:
        t=pattern.sub(r"\1\1", t)
    return tweet_tokens

def cleanMetachars(tweet):
    return tweet

#===============TOKENIZATION===============
def tokenizetweet(tweet):
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
def processTweetText(tweet):
    tweet=encodeStream(tweet)

    tweet=removeUrl(tweet)
    tweet=removeMentions(tweet)
    tweet=removeHashtags(tweet)

    tweet=removeWhitespace(tweet)
    tweet=removePunctuation(tweet)
    #tweet=replaceRepeats_gt2(tweet)

    tokens=tokenizetweet(tweet)
    #tokens=translateSlangs(tokens)
    tokens=removeStopWords(tokens)
    return tokens

#__name__ = '__streamfilters__'

def testTweetProcessor():
    #partially working, doesn't seem to work on urls w/o http
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
    whitespace_test="    The @SEC was    7th in Conference RPI during the regular season. They’re 7-0 in the NCAA Tournament. #MarchMadness   "
    print 'removeWhitespace BEFORE:', whitespace_test
    print 'removeWhitespace AFTER:', removeWhitespace(whitespace_test)

    #TODO
    metachar_test="new\nline\ntwee..\n\n..eet"
    print 'cleanMetachars BEFORE:', metachar_test
    print 'cleanMetachars AFTER:', cleanMetachars(metachar_test)

    #Doesn't work
    punctuation_test="Ohhh Shittt...it's missed gym o'clock again...FUCK!!\n*cracks 3rd beer"
    print 'removePunctuation BEFORE:', punctuation_test
    print 'removePunctuation AFTER:', removePunctuation(punctuation_test)

    #Doesn't work
    repeats_test="Ohhh Shittt it's missed gym o'clock again...FUCKKKK!!\n*cracks 3rd beer"
    print 'replaceRepeats_gt2 BEFORE:', repeats_test
    print 'replaceRepeats_gt2 AFTER:', replaceRepeats_gt2(repeats_test.split())


    stopword_test='anybody considering best inward several provided'
    stopword_test_tokens=stopword_test.split()
    print 'removeStopWords BEFORE:', stopword_test_tokens
    print 'removeStopWords AFTER:', removeStopWords(stopword_test_tokens)

    #slangword_test=''

if __name__ == '__main__':
    testTweetProcessor()
