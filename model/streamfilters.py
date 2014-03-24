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
    tweet=unicode(tweet,'utf-8')
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
    return tweet

def replaceRepeats_gt2(tweet):
    pattern=re.compile(r"(.)\1{1,}", re.DOTALL)
    tweet=pattern.sub(r"\1\1", s)
    return tweet

#===============TOKENIZATION===============
def tokenizetweet(tweet):
    return [t for t in tweet.split(' ') if t is not '']

#===============STOPWORDS===============
def getAllStopwords():
    allStopWordsFile=os.path.join(os.path.join(os.path.join(os.path.abspath(os.path.pardir),'resources'),'stopwords'),'all_stopwords.txt')
    return [sw for sw in open(allStopWordsFile,'r')]

def removeStopWords(tweet_tokens):
    stopwords_list=getAllStopwords()
    after_stopwords=[tok for tok in tweet_tokens if tok not in stopwords_list]
    return tweet

#===============SLANGS===============
def getSlangDictionary():
    allSlangWordsFile=os.path.join(os.path.join(os.path.join(os.path.abspath(os.path.pardir),'resources'),'slangwords'),'all_slangwords.txt')
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
    tweet=replaceRepeats_gt2(tweet)

    tokens=tokenizetweet(tweet)
    tokens=translateSlangs(tokens)
    tokens=removeStopWords(tokens)
    return tokens
