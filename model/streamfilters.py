import re
from collections import defaultdict
import sys
import os
from unidecode import unidecode

    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')

def encodeStream(tweet):
    tweet=unicode(tweet,'utf-8')
    tweet=unidecode(tweet)
    tweet=tweet.lower()
    return tweet

def removeUrl(tweet):
    tweet=re.sub('((www\.[\s]+)|(https?://[^\s]+))','',tweet)
    return tweet

def removeMentions(tweet):
    tweet = re.sub('@[^\s]+','',tweet)
    return tweet

def removeHashtags(tweet):
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    return tweet

def removeWhitespace(tweet):
    tweet = re.sub('[\s]+', ' ', tweet)
    return tweet

def removeStopWords(tweet):
    return tweet

def parseLulz(tweet):
    return tweet

def replaceRepeats_gt2(tweet):
    pattern=re.compile(r"(.)\1{1,}", re.DOTALL)
    tweet=pattern.sub(r"\1\1", s)
    return tweet

def removePunctuation(tweet):
    tweet=tweet.strip('\'"')
    tweet=tweet.strip('\'"?,.')
    return tweet
