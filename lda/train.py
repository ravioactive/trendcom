# Steps towards an LDA model:
# [[tokens]] -> {dictionary} -> [[bow_(id,freq)]]  ->   [lda model]     ->    similarity
#                                   corpus            transformation        Jensen-Shannon
#                               serialize to disk                          May need to implement

from gensim import corpora, models, similarities
from resources import globalobjs
import tweetcorpus
import operator
import itertools
import sys
import numpy
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
globalobjs.init()


def createBOWCorpus(corpus, dictionary):
    trend_corpus_bow = tweetcorpus.corpus_bow_iter(corpus, dictionary)
    return trend_corpus_bow


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

    modelName = globalobjs.getLdaObjFileName(trend + opt_suffix, globalobjs.MODEL)
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


def trainer_new():
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

    # trend_corpus = createCorpus(trend)
    # trendDict = createDictionary(trend, trend_corpus)
    # print trendDict
    # bow_corpus = createBOWCorpus(trend_corpus, trendDict)
    # # saveDictionary(trend, trendDict)
    # # saveBOWCorpus(trend, bow_corpus)

    # lda = asLda(bow_corpus, trendDict, numtopics, numupdates, doc_chunk, corpus_passes)
    # lda.print_topics(numtopics)

    lda = train(trend, numtopics, numupdates, doc_chunk, corpus_passes)
    lda.print_topics(numtopics)

    return lda
    all_topics = lda.state.get_lambda()
    for x in xrange(lda.num_topics):
        topic = all_topics[x]
        print "TOPIC LENGTH: ", len(topic)
        topic = topic / topic.sum()  # normalize to probability dist
        bestn = numpy.argsort(topic)[::-1][:10]  # top 10 terms
        bestnprob = [topic[num] for num in bestn]  # top 10 probabilities
        bestn = [lda.id2word[num] for num in bestn]  # top 10 terms text
        print "MODEL: ", bestn
        print "TOPIC: ", bestnprob

    # optStr = "_online_"
    # if numupdates == 0:
    #     optStr = "_batch_"
    # saveLdaModel(trend, lda, updates= lda.num_updates, topics = lda.num_topics, optional = optStr)


def train(trend, topics, updates, chunksize, passes):
    trend_corpus = createCorpus(trend)
    trendDict = createDictionary(trend, trend_corpus)
    print trendDict
    bow_corpus = createBOWCorpus(trend_corpus, trendDict)
    # saveDictionary(trend, trendDict)
    # saveBOWCorpus(trend, bow_corpus)

    lda = asLda(bow_corpus, trendDict, topics, updates, chunksize, passes)
    return lda


def compareTrends():
    numtopics = globalobjs.num_topics_lda
    numupdates = globalobjs.update_freq
    doc_chunk = globalobjs.lda_chunk_size
    corpus_passes = globalobjs.passes_corpus

    args = sys.argv[1:]
    if len(args) < 1:
        print "Missing argument <trend>"
        print "Model Trainer usage:\n<trend1>\n<trend2>\n<numtopics>\n<numupdates>\n<chunksize>\n<numpasses>"
        sys.exit(1)
    trend1 = args[0]
    trend2 = args[1]
    if not trend1 or trend1 == '' or not trend2 or trend2 == '':
        print "Illeagal value for argument <trend1> or <trend2>"
        sys.exit(1)

    lda1 = train(trend1, numtopics, numupdates, doc_chunk, corpus_passes)
    lda2 = train(trend2, numtopics, numupdates, doc_chunk, corpus_passes)

    similarTopics = getSimilarTopics(lda1, lda2)
    print similarTopics


def getSimilarTopics(model1, model2):
    simTopics = list()
    # TODO: handle number of topics to compare
    alltopics1 = model1.state.get_lambda()
    alltopics2 = model2.state.get_lambda()
    for i in xrange(alltopics1.num_topics):
        topic1 = alltopics1[i]
        topic1 = topic1 / topic1.sum()
        alltokens1 = numpy.argsort(topic1)[::-1][:]
        alltokensProbs1 = [topic1[num] for num in alltokens1]
        minJS = -sys.maxint - 1
        minJSidx = 0
        for j in xrange(alltopics2.num_topics):
            topic2 = alltopics2[j]
            topic2 = topic2 / topic2.sum()
            alltokens2 = numpy.argsort(topic2)[::-1][:]
            alltokensProbs2 = [topic2[num] for num in alltokens2]
            jsDiv = getJSDivergence(alltokensProbs1, alltokensProbs2)
            if jsDiv < minJS:
                minJS = jsDiv
                minJSidx = j
        simTopics.append((i, minJSidx, minJS))  # pushing in to a list of tuples?
    return simTopics


def getKLDivergence(dist1, dist2):
    p = numpy.asarray(dist1, dtype=numpy.float)
    q = numpy.asarray(dist2, dtype=numpy.float)
    return numpy.sum(numpy.where(p != 0, p * numpy.log(p / q), 0))

# average[x] = weight * p[x] + (1 - weight) * q[x]
# self.JSD = (weight * self.KL_divergence(array(p), average)) + ((1 - weight) * self.KL_divergence(array(q), average))
def getJSDivergence(dist1, dist2):
    weight = 0.5
    p = numpy.asarray(dist1, dtype=numpy.float)
    q = numpy.asarray(dist2, dtype=numpy.float)
    a = numpy.zeros(len(p))
    for i in xrange(len(p)):
        a[i] = weight * p[i] + (1 - weight) * q[i]
    jsd = (weight * getKLDivergence(p, a)) + ((1 - weight) * getKLDivergence(q, a))
    return 1 - jsd/numpy.sqrt(2 * numpy.log10(2))


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
    trainer_new()
