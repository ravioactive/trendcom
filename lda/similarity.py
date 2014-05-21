# from gensim import corpora, models, similarities
# import tweetcorpus
# import operator
# import itertools
import sys
import numpy
import logging
from datetime import datetime
from scipy import stats
import ldamodel
from resources import globalobjs

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
globalobjs.init()

# TODO:
# Handle all variations in lda parameters to be taken from command line args
# numtopics, numupdates, doc_chunk, corpus_passes
# offset, corpus length
# filters from command line


def comparison(trend1, trend2, metric = "JS", filters1 = None, filters2 = None):
    numtopics = globalobjs.num_topics_lda
    numupdates = globalobjs.update_freq
    doc_chunk = globalobjs.lda_chunk_size
    corpus_passes = globalobjs.passes_corpus

    start = datetime(2014, 4, 26)
    # filters1 = {"timestamp": {"$gt": start}}
    filters1 = None
    lda1 = ldamodel.train(trend1, numtopics, numupdates, doc_chunk, corpus_passes, filters1)

    # filters2 = {"timestamp": {"$lt": start}}
    filters2 = None
    lda2 = ldamodel.train(trend2, numtopics, numupdates, doc_chunk, corpus_passes, filters2, lda1.state.numdocs)

    similarTopics = list()
    if metric == "KT":
        similarTopics = getCommonTokens(lda1, lda2)
    elif metric == "JSKT":
        similarTopics = getKTofSimByJS(lda1, lda2, getSimilarTopics(lda1, lda2))
    elif metric == "KTJS":
        similarTopics = getJSofSimByKT(lda1, lda2, getCommonTokens(lda1, lda2))
    else:
        similarTopics = getSimilarTopics(lda1, lda2)

    printSimilarTopics(similarTopics, metric)


def printSimilarTopics(similarTopics, metric = ""):
    simTopicsTupleLen = len(similarTopics[0][2:])
    simSum = [0] * simTopicsTupleLen
    print simTopicsTupleLen, len(simSum), simSum
    for i in xrange(len(similarTopics)):
        print similarTopics[i]
        if len(simSum) > 0:
            for j in range(len(simSum)):
                simSum[j] += similarTopics[i][2 + j]
    print "Sum of all metrics by", metric, ":", simSum
    print "Average of all metrics by", metric, ":", [x/len(similarTopics) for x in simSum]



def getSimilarTopics(model1, model2):
    simTopics = list()
    # TODO: handle number of topics to compare
    alltopics1 = model1.state.get_lambda()
    alltopics2 = model2.state.get_lambda()
    if model1.num_topics <= model2.num_topics:
        minTopics = model1.num_topics
    else:
        minTopics = model2.num_topics
    #for i in xrange(model1.num_topics):
    for i in xrange(minTopics):
        topic1 = alltopics1[i]
        topic1 = topic1 / topic1.sum()
        alltokens1 = numpy.argsort(topic1)[::-1][:]
        alltokensProbs1 = [topic1[num] for num in alltokens1]
        # print
        print "Finding similar topic for topic", i
        tenTokens1Strs = [model1.id2word[num] for num in alltokens1[:10]]
        print tenTokens1Strs

        minJS = sys.maxint
        minJSidx = 0
        # for j in xrange(model2.num_topics):
        for j in xrange(minTopics):
            topic2 = alltopics2[j]
            topic2 = topic2 / topic2.sum()
            alltokens2 = numpy.argsort(topic2)[::-1][:]
            alltokensProbs2 = [topic2[num] for num in alltokens2]
            jsDiv = getJSDivergence(alltokensProbs1, alltokensProbs2)
            if jsDiv < minJS:
                minJS = jsDiv
                minJSidx = j
        simTopics.append((i, minJSidx, minJS))  # pushing in to a list of tuples?
        minJSTopic = alltopics2[minJSidx]
        minJSTopic = minJSTopic / minJSTopic.sum()
        # print
        tenMinJSTokens = numpy.argsort(minJSTopic)[::-1][:10]
        minJSTokenStrs = [model2.id2word[num] for num in tenMinJSTokens]
        print minJSTokenStrs
    return simTopics


def getKTofSimByJS(model1, model2, similarTopicsByJS):
    print "Finding Kendall Tau of topics similar by JS Divergence"
    word2id1 = model1.id2word.token2id
    word2id2 = model2.id2word.token2id
    common = set(word2id1.keys()) & set(word2id2.keys())
    print "Number of common Tokens", len(common)

    alltopics1 = model1.state.get_lambda()
    alltopics2 = model2.state.get_lambda()
    for i in xrange(len(similarTopicsByJS)):
        tup = similarTopicsByJS[i]
        topic1 = alltopics1[tup[0]]
        topic1 = topic1 / topic1.sum()
        alltokens1 = numpy.argsort(topic1)[::-1][:]
        commonIdxs1 = [numpy.where(alltokens1 == model1.id2word.token2id[cmn])[0][0] for cmn in common]
        topic2 = alltopics2[tup[1]]
        topic2 = topic2 / topic2.sum()
        alltokens2 = numpy.argsort(topic2)[::-1][:]
        commonIdxs2 = [numpy.where(alltokens2 == model2.id2word.token2id[cmn])[0][0] for cmn in common]
        KT, p = stats.kendalltau(commonIdxs1, commonIdxs2)
        print KT, p
        similarTopicsByJS[i] += (KT, p)
        print similarTopicsByJS[i]
    return similarTopicsByJS


def getJSofSimByKT(model1, model2, similarTopicsByKT):
    print "Finding JS Divergence of topics similar by Kendall Tau"
    alltopics1 = model1.state.get_lambda()
    alltopics2 = model2.state.get_lambda()
    for i in xrange(len(similarTopicsByKT)):
        tup = similarTopicsByKT[i]
        topic1 = alltopics1[tup[0]]
        topic1 = topic1 / topic1.sum()
        alltokens1 = numpy.argsort(topic1)[::-1][:]
        alltokensProbs1 = [topic1[num] for num in alltokens1]

        topic2 = alltopics2[tup[1]]
        topic2 = topic2 / topic2.sum()
        alltokens2 = numpy.argsort(topic2)[::-1][:]
        alltokensProbs2 = [topic2[num] for num in alltokens2]
        JS = getJSDivergence(alltokensProbs1, alltokensProbs2)
        similarTopicsByKT[i] += (JS,)
        print similarTopicsByKT[i]
    return similarTopicsByKT


def getKLDivergence(dist1, dist2):
    p = numpy.asarray(dist1, dtype=numpy.float)
    q = numpy.asarray(dist2, dtype=numpy.float)
    return numpy.sum(numpy.where(p != 0, p * numpy.log(p / q), 0))


def getJSDivergence(dist1, dist2):
    weight = 0.5
    p = numpy.asarray(dist1, dtype=numpy.float)
    q = numpy.asarray(dist2, dtype=numpy.float)
    if len(p) <= len(q):
        normLen = len(p)
    else:
        normLen = len(q)
    p = p[:normLen]
    q = q[:normLen]
    a = numpy.zeros(normLen)
    for i in xrange(normLen):
        a[i] = weight * p[i] + (1 - weight) * q[i]
    jsd = (weight * getKLDivergence(p, a)) + ((1 - weight) * getKLDivergence(q, a))
    # return 1 - jsd/numpy.sqrt(2 * numpy.log10(2))
    return jsd


def getCommonTokens(model1, model2):
    simTopics = list()
    word2id1 = model1.id2word.token2id
    word2id2 = model2.id2word.token2id
    common = set(word2id1.keys()) & set(word2id2.keys())
    print "Number of common Tokens", len(common)
    alltopics1 = model1.state.get_lambda()
    alltopics2 = model2.state.get_lambda()

    if model1.num_topics <= model2.num_topics:
        minTopics = model1.num_topics
    else:
        minTopics = model2.num_topics
    #for i in xrange(model1.num_topics):
    for i in xrange(minTopics):
        topic1 = alltopics1[i]
        topic1 = topic1 / topic1.sum()
        alltokens1 = numpy.argsort(topic1)[::-1][:]
        commonIdxs1 = [numpy.where(alltokens1 == model1.id2word.token2id[cmn])[0][0] for cmn in common]

        print "Finding Max. Kendall Tau for topic", i
        # print list(common)[:25]
        # print commonIdxs1[:25]
        # print [model1.id2word[alltokens1[idx]] for idx in commonIdxs1[:25]]
        tenTokens1Strs = [model1.id2word[num] for num in alltokens1[:10]]
        print tenTokens1Strs

        maxKT = - sys.maxint - 1
        maxKTidx = 0

        for j in xrange(minTopics):
            topic2 = alltopics2[j]
            topic2 = topic2 / topic2.sum()
            alltokens2 = numpy.argsort(topic2)[::-1][:]
            commonIdxs2 = [numpy.where(alltokens2 == model2.id2word.token2id[cmn])[0][0] for cmn in common]
            # print list(common)[:25]
            # print commonIdxs2[:25]
            # print [model2.id2word[alltokens2[idx]] for idx in commonIdxs2[:25]]

            KT, p = stats.kendalltau(commonIdxs1, commonIdxs2)
            if KT > maxKT:
                maxKT = KT
                maxKTidx = j

        simTopics.append((i, maxKTidx, maxKT))
        maxKTTopic = alltopics2[maxKTidx]
        maxKTTopic = maxKTTopic / maxKTTopic.sum()

        tenMaxKTTokens = numpy.argsort(maxKTTopic)[::-1][:10]
        maxKTTokenStrs = [model2.id2word[num] for num in tenMaxKTTokens]
        print maxKTTokenStrs

    return simTopics


def compareTrends():
    args = sys.argv[1:]
    if len(args) < 1:
        print "Missing arguments <trend1> <trend2>"
        print "Model Trainer usage: <trend1> <trend2> <numtopics> <numupdates> <chunksize> <numpasses>"
        sys.exit(1)
    if len(args) < 2:
        print "Missing arguments <trend1>"
        print "Model Trainer usage: <trend1> <trend2> <numtopics> <numupdates> <chunksize> <numpasses>"
        sys.exit(1)

    trend1 = args[0]
    trend2 = args[1]

    if not trend1 or trend1 == '' or not trend2 or trend2 == '':
        print "Illeagal value for argument <trend1> or <trend2>"
        sys.exit(1)

    metric = "JS"
    if len(args) >= 3:
        metric = args[2]
    comparison(trend1, trend2, metric)


if __name__ == '__main__':
    compareTrends()
