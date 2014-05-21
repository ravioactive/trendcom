# Steps towards an LDA model:
# [[tokens]] -> {dictionary} -> [[bow_(id,freq)]]  ->   [lda model]     ->    similarity
#                                   corpus            transformation        Jensen-Shannon
#                               serialize to disk                          May need to implement
# -*- coding: utf-8 -*-
from gensim import corpora, models
from resources import globalobjs
import tweetcorpus
import operator
import itertools
import sys
import numpy
import logging
import similarity
from unidecode import unidecode

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
globalobjs.init()


def createBOWCorpus(corpus, dictionary):
    trend_corpus_bow = tweetcorpus.corpus_bow_iter(corpus, dictionary)
    return trend_corpus_bow


def createCorpus(trend, filters = None, limit = None):
    trend_corpus = tweetcorpus.corpus_iter(trend, globalobjs.db, filters, limit)
    return trend_corpus

def createRankCorpus(trend, filters = None, limit = None):
    rank_corpus = tweetcorpus.rank_corpus(trend, globalobjs.db, filters, limit)
    return rank_corpus

def getTrendStopWordIds(trend, corpDict):
    stopWordsForTrend = globalobjs.getTrendStopWords(trend)
    return [corpDict.token2id[stopword] for stopword in stopWordsForTrend if stopword in corpDict.token2id]


def createDictionary(trend, corpus):
    corpusDictionary = corpora.Dictionary(corpus)
    stopWordIds = getTrendStopWordIds(trend, corpusDictionary)
    corpusDictionary.filter_tokens(stopWordIds)
    numericTokenIds = getIdsForNumericTokens(corpusDictionary)
    corpusDictionary.filter_tokens(numericTokenIds)
    corpusDictionary.compactify()
    return corpusDictionary


def saveDictionary(trend, dictionary):
    dictName = globalobjs.getLdaObjFileName(trend, globalobjs.DICT)
    if dictName == "":
        return False
    else:
        dictionary.save(dictName)
        return True


def saveBOWCorpus(trend, bowcorpus, extn = globalobjs.MM_CORPUS_TYPE):
    corpusName = globalobjs.getLdaObjFileName(trend, globalobjs.CORPUS, extn = extn)
    if corpusName == "":
        return False

    if(extn == globalobjs.MM_CORPUS_TYPE):
        corpora.MmCorpus.serialize(corpusName, bowcorpus)
    elif(extn == globalobjs.BLEI_CORPUS_TYPE):
        corpora.BleiCorpus.serialize(corpusName, bowcorpus)
    elif(extn == globalobjs.SVMLIGHT_CORPUS_TYPE):
        corpora.SvmLightCorpus.serialize(corpusName, bowcorpus)
    elif(extn == globalobjs.LOW_CORPUS_TYPE):
        corpora.LowCorpus.serialize(corpusName, bowcorpus)


def getBOWCorpusFromFile(name, extn=globalobjs.MM_CORPUS_TYPE):
    disk_bowcorpus = None
    validName = globalobjs.validatedLdaFileName(name, extn)
    if validName == "":
        return disk_bowcorpus

    if(extn == globalobjs.MM_CORPUS_TYPE):
        disk_bowcorpus = corpora.MmCorpus(validName)
    elif(extn == globalobjs.BLEI_CORPUS_TYPE):
        disk_bowcorpus = corpora.BleiCorpus(validName)
    elif(extn == globalobjs.SVMLIGHT_CORPUS_TYPE):
        disk_bowcorpus = corpora.SvmLightCorpus(validName)
    elif(extn == globalobjs.LOW_CORPUS_TYPE):
        disk_bowcorpus = corpora.LowCorpus(validName)

    return disk_bowcorpus


def getDictionaryFromFile(name, extn=""):
    disk_dictionary = None
    validName = globalobjs.validatedLdaFileName(name, globalobjs.DICT_FILE_TYPE)
    if validName == "":
        return disk_dictionary

    disk_dictionary = corpora.Dictionary.load(validName)
    return disk_dictionary


def asTfIdf(corpus):
    tfidf = models.TfidfModel(corpus)
    return tfidf


def asLda(corpus, dictionary, numtopics, updatefreq = globalobjs.update_freq, chunksz = 2000, num_passes = globalobjs.passes_corpus):
    corpus.rewind()
    lda = models.ldamodel.LdaModel(corpus = list(corpus), id2word = dictionary, num_topics = numtopics, chunksize = chunksz, update_every = updatefreq, passes = num_passes)
    return lda


def saveLdaModel(trend, ldamodel, **kwargs):
    updates, topics, optional, opt_suffix = "", "", "", ""
    if "updates" in kwargs:
        updates = kwargs['updates']
        opt_suffix += "-up" + str(updates)
    if "topics" in kwargs:
        topics = kwargs['topics']
        opt_suffix += "-topics" + str(topics)
    if "optional" in kwargs:
        optional = kwargs['optional']
        opt_suffix += str(optional)
    optStr = "_online_"
    if lda.numupdates == 0:
        optStr = "_batch_"
    modelName = globalobjs.getLdaObjFileName(trend + opt_suffix + optStr, globalobjs.MODEL)
    if modelName == "":
        return False

    ldamodel.save(modelName)


def getModelFromFile(name, extn=globalobjs.LDA_MODEL_TYPE):
    disk_model = None
    validName = globalobjs.validatedLdaFileName(name, extn)
    if validName == "":
        return disk_model

    if(extn == globalobjs.LDA_MODEL_TYPE):
        disk_model = models.ldamodel.LdaModel.load(validName)

    return disk_model



def train(trend, topics, updates, chunksize, passes, filters = None, limit = None):
    trend_corpus = createCorpus(trend, filters, limit)
    trendDict = createDictionary(trend, trend_corpus)
    print trendDict
    bow_corpus = createBOWCorpus(trend_corpus, trendDict)
    lda = asLda(bow_corpus, trendDict, topics, updates, chunksize, passes)
    return lda


def trainer_load(dictFileName, bowCorpusFileName, **kwargs):
    savedDictionary = getDictionaryFromFile(dictFileName)
    print savedDictionary
    extn = globalobjs.MM_CORPUS_TYPE
    if "corpextn" in kwargs:
        extn = kwargs["corpextn"]
    savedBowCorpus = getBOWCorpusFromFile(bowCorpusFileName, extn)
    print savedBowCorpus


def getIdsForNumericTokens(d):
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


def newTrend():
    numtopics = globalobjs.num_topics_lda
    numupdates = globalobjs.update_freq
    doc_chunk = globalobjs.lda_chunk_size
    corpus_passes = globalobjs.passes_corpus

    args = sys.argv[1:]
    trend = None
    if len(args) < 1:
        print "Missing argument <trend>"
        print "Model Trainer usage: <trend> <numtopics> <numupdates> <chunksize> <numpasses>"
        sys.exit(1)

    trend = args[0]
    if not trend or trend == '':
        print "Illeagal value for argument <trend>"
        sys.exit(1)

    if len(args) >= 2:
        numtopics = int(args[1])
        print "Given number of topics:", numtopics
        if len(args) >= 2:
            numupdates = int(args[2])
            print "Given number of updates:", numupdates
            if len(args) >= 3:
                doc_chunk = int(args[3])
                print "Given chunk size:", doc_chunk
                if len(args) >= 4:
                    corpus_passes = int(args[4])
                    print "Given number of passes:", corpus_passes
                else:
                    print "Using default number of passes (1)"
            else:
                print "Using default chunk size (2000)"
                print "Using default number of passes (1)"
        else:
            print "Using default number of updates (1 - online)"
            print "Using default chunk size (2000)"
            print "Using default number of passes (1)"
    else:
        print "Using default number of topics (35)"
        print "Using default number of updates (1 - online)"
        print "Using default chunk size (2000)"
        print "Using default number of passes (1)"

    # start = datetime(2014, 4, 26)
    # filters = {"timestamp": {"$gt": start}}
    filters = None
    # limit = 20000
    limit = None
    lda = train(trend, numtopics, numupdates, doc_chunk, corpus_passes, filters, limit)
    lda.print_topics(numtopics)

    new_corpus = createCorpus(trend, filters, limit)
    new_bow_corpus = createBOWCorpus(new_corpus, lda.id2word)
    new_rank_corpus = createRankCorpus(trend, filters, limit)

    new_lda_corpus = lda[new_bow_corpus]
    zipped = zip(new_rank_corpus, new_lda_corpus)

    new_bow_corpus.rewind()
    for i in xrange(lda.num_topics):
        tops = sorted(zipped, reverse=True, key=lambda doc: abs(dict(doc[1]).get(i, 0.0)))
        print "\nTop Tweets for TOPIC", i, lda.print_topic(i, 10)
        getTopTweets(tops, 5)
        new_bow_corpus.rewind()

    # return lda


def getTopTweets(tops, n):
    topN = tops[:n]
    for t in topN:
        tweet = tweetcorpus.getDoc(t[0], globalobjs.db)
        print "TWEET:", unidecode(tweet['text'])
        # print tweet['tokens']

if __name__ == '__main__':
    newTrend()
    # corpusTest()
