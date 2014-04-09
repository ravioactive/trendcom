# Steps towards an LDA model:
# [[tokens]] -> {dictionary} -> [[bow_(id,freq)]]  ->   [lda model]     ->    similarity
#                                   corpus            transformation        Jensen-Shannon
#                               serialize to disk                          May need to implement

from gensim import corpora
from resources import globals
import tweetcorpus
import operator
import itertools


def bowtrainer(trend):
    globals.init()
    trend_corpus = tweetcorpus.corpus_iter(trend, globals.db)
    print 'tweetcorpus', trend_corpus
    trendDict = corpora.Dictionary(trend_corpus)
    # trend_corpus_bow = tweetcorpus.corpus_bow_iter(trend_corpus, trendDict)
    trend_corpus_bow = tweetcorpus.corpus_bow_iter(trend, globals.db, trendDict)


def trainer(trend):
    globals.init()
    trend_corpus = tweetcorpus.corpus_iter(trend, globals.db)
    print 'tweetcorpus', trend_corpus
    trendDict = corpora.Dictionary(trend_corpus)
    print "Number of tokens", len(trendDict.keys())
    numericTokenIds = getNumIds(trendDict)
    trendDict.filter_tokens(numericTokenIds)
    trendDict.compactify()
    print(trendDict)

#def persist_corpus(trend, corpus, dictionary):



def getNumIds(d):
    t2id = d.token2id
    numids = [numtokid for numtok, numtokid in t2id.iteritems() if is_number(numtok)]
    return numids


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def getTopK(d, k):
    id2token = {v: k for k, v in d.token2id.iteritems()}
    sorted_d = sorted(d.dfs.iteritems(), key=operator.itemgetter(1), reverse=True)
    for k, v in itertools.islice(sorted_d, 0, k):
        print v, ":", id2token[k], ":", k


def findKFreq(d, k):
    tokenIds = {t: f for t, f in d.dfs.iteritems() if f >= k}
    d2id = d.token2id
    wordFreqs = {d2id[t]: f for t, f in tokenIds}
    for k, v in wordFreqs.iteritems():
        print k, ":", v

if __name__ == '__main__':
    bowtrainer('#mh370')
