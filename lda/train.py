# Steps towards an LDA model:
# [[tokens]] -> {dictionary} -> [[bow_(id,freq)]]  ->   [lda model]     ->    similarity
#                                   corpus            transformation        Jensen-Shannon
#                               serialize to disk                          May need to implement

from gensim import corpora, models, similarities
from resources import globalobjs
import tweetcorpus
import operator
import itertools
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
globalobjs.init()


def createBOWCorpus(corpus, dictionary):
    trend_corpus_bow = tweetcorpus.corpus_bow_iter(corpus, dictionary)
    return trend_corpus_bow


def freshBOWCorpus(bowcorpus):
    return tweetcorpus.corpus_bow_iter(bowcorpus)


def createCorpus(trend):
    trend_corpus = tweetcorpus.corpus_iter(trend, globalobjs.db)
    return trend_corpus


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
    lda = models.ldamodel.LdaModel(corpus = corpus, id2word = dictionary, num_topics = numtopics, chunksize = chunksz, update_every = updatefreq, passes = num_passes)
    return lda


def saveLdaModel(trend, ldamodel):
    modelName = globalobjs.getLdaObjFileName(trend, globalobjs.MODEL)
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


def trainer_new(trend):
    print "has inited? ", globalobjs.isInit()
    trend_corpus = createCorpus(trend)
    trendDict = createDictionary(trend, trend_corpus)
    print trendDict
    bow_corpus = createBOWCorpus(trend_corpus, trendDict)
    saveDictionary(trend, trendDict)
    saveBOWCorpus(trend, bow_corpus)
    lda_static = asLda(bow_corpus, trendDict, globalobjs.num_topics_lda, 0, 2000, 20)
    lda_static.print_topics(10, 20)
    saveLdaModel(trend, lda_static)

    fresh_bow_corpus = freshBOWCorpus(bow_corpus)
    lda_online = asLda(fresh_bow_corpus, trendDict, globalobjs.num_topics_lda)
    lda_online.print_topics(10, 20)
    saveLdaModel(trend, lda_online)


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

if __name__ == '__main__':
    trainer_new('#mh370')
