# Steps towards an LDA model:
# [[tokens]] -> {dictionary} -> [[bow_(id,freq)]]  ->   [lda model]     ->    similarity
#                                   corpus            transformation        Jensen-Shannon
#                               serialize to disk                          May need to implement

from gensim import corpora
from resources import globals
import tweetcorpus
import operator
import itertools


def createBOWCorpus(corpus, dictionary):
    trend_corpus_bow = tweetcorpus.corpus_bow_iter(trend_corpus, trendDict)
    return trend_corpus_bow


def createCorpus(trend):
    trend_corpus = tweetcorpus.corpus_iter(trend, globals.db)
    return trend_corpus


def createDictionary(corpus):
    trendDict = corpora.Dictionary(corpus)
    return trendDict


def saveDictionary(trend, dictionary):
    dictName = globals.getLdaObjFileName(trend, globals.DICT)
    if dictName == "":
        return False
    else:
        dictionary.save(dictName)
        return True


def saveBOWCorpus(trend, bowcorpus, extn=globals.MM_CORPUS_TYPE):
    corpusName = globals.getLdaObjFileName(trend, globals.CORPUS, extn)
    if corpusName == "":
        return False

    if(extn == globals.MM_CORPUS_TYPE):
        corpora.MmCorpus.serialize(corpusName, bowcorpus)
    elif(extn == globals.BLEI_CORPUS_TYPE):
        corpora.BleiCorpus.serialize(corpusName, bowcorpus)
    elif(extn == globals.SVMLIGHT_CORPUS_TYPE):
        corpora.SvmLightCorpus.serialize(corpusName, bowcorpus)
    elif(extn == globals.LOW_CORPUS_TYPE):
        corpora.LowCorpus.serialize(corpusName, bowcorpus)


def getBOWCorpusFromFile(name, extn=globals.MM_CORPUS_TYPE):
    disk_bowcorpus = None
    validName = globals.validatedLdaFileName(name, extn)
    if validName == "":
        return disk_bowcorpus

    if(extn == globals.MM_CORPUS_TYPE):
        disk_bowcorpus = corpora.MmCorpus(validName)
    elif(extn == globals.BLEI_CORPUS_TYPE):
        disk_bowcorpus = corpora.BleiCorpus(validName)
    elif(extn == globals.SVMLIGHT_CORPUS_TYPE):
        disk_bowcorpus = corpora.SvmLightCorpus(validName)
    elif(extn == globals.LOW_CORPUS_TYPE):
        disk_bowcorpus = corpora.LowCorpus(validName)

    return disk_bowcorpus


def getDictionaryFromFile(name, extn=""):
    disk_dictionary = None
    validName = globals.validatedLdaFileName(name, globals.DICT_FILE_TYPE)
    if validName == "":
        return disk_dictionary

    disk_dictionary = corpora.Dictionary.load(validName)
    return disk_dictionary


def bowtrainer(trend):
    globals.init()
    trend_corpus = tweetcorpus.corpus_iter(trend, globals.db)
    print 'tweetcorpus', trend_corpus
    trendDict = corpora.Dictionary(trend_corpus)
    # trend_corpus_bow = tweetcorpus.corpus_bow_iter(trend_corpus, trendDict)
    trend_corpus_bow = tweetcorpus.corpus_bow_iter(trend, globals.db, trendDict)
    print trend_corpus_bow

def trainer_new(trend):
    globals.init()
    trend_corpus = createCorpus(trend)
    trendDict = createDictionary(trend_corpus)
    numericTokenIds = getIdsForNumericTokens(trendDict)
    trendDict.filter_tokens(numericTokenIds)
    trendDict.compactify()
    bow_corpus = createBOWCorpus(trend_corpus, trendDict)
    saveDictionary(trend, trendDict)
    saveBOWCorpus(trend, bow_corpus)

def trainer_load(dictFileName, bowCorpusFileName, **kwargs):
    savedDictionary = getDictionaryFromFile(dictFileName)
    print savedDictionary
    extn = globals.MM_CORPUS_TYPE
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

if __name__ == '__main__':
    trainer_new('#mh370')
