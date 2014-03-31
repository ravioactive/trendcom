# -*- coding: utf-8 -*-
import re
import os
import pymongo
import time
import datetime
import keys

def init():
    global consumer_key
    consumer_key = keys.x_consumer_key
    global consumer_secret
    consumer_secret = keys.x_consumer_secret
    global access_token
    access_token = keys.x_access_token
    global access_token_secret
    access_token_secret = keys.x_access_token_secret

    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    global db
    db = connection.trendcom

    global urlpat
    urlpat = re.compile(r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
    global mentionpat
    mentionpat = re.compile(r"@[^\s]+")
    global hastagpat
    hastagpat = re.compile(r'#([^\s]+)')
    global metapunctpat
    metapunctpat = re.compile('[^a-zA-Z0-9]+')
    global repeatgrp1
    repeatgrp1 = re.compile(r"(.)\1{2,}", re.DOTALL)
    global repeatgrp2
    repeatgrp2 = re.compile(r"(..)\1{2,}", re.DOTALL)
    global repeatsubspat
    repeatsubspat = r"\1\1"
    global stopwords_list
    stopwords_list = getAllStopwords()
    global slangDict
    #slangDict=getSlangDictionary()
    global logfile
    logfile = getLogFile()
    global ts_beg
    ts_beg = datetime.datetime.now()

def getUptime():
    ts_now = datetime.datetime.now()
    ts_diff = ts_now - ts_beg
    return ts_diff

def getAllStopwords():
    allStopWordsFilePath=os.path.join(os.path.join(os.path.join(os.path.join(os.path.abspath(os.path.pardir),'code'),'resources'),'stopwords'),'all_stopwords.txt')
    f = open(allStopWordsFilePath,'r')
    lines = f.read().splitlines()
    f.close()
    return lines

def getSlangDictionary():
    allSlangWordsFilePath=os.path.join(os.path.join(os.path.join(os.path.join(os.path.abspath(os.path.pardir),'code'),'resources'),'slangwords'),'all_slangwords.txt')
    f = open(allSlangWordsFilePath,'r')
    keyvalues = {k:v for (k,v) in [slw.split(':') for slw in f]}
    f.close()
    return keyvalues

def getLogFile():
    logDir = os.path.join(os.path.join(os.path.abspath(os.path.pardir),'code'),'logs')
    stdlogfilename = os.path.join(logDir, 'current.log')
    stdlogfilefound = os.path.isfile(stdlogfilename)
    if(stdlogfilefound):
        ts_suffix = datetime.datetime.fromtimestamp(os.path.getctime(stdlogfilename)).strftime("%Y-%m-%d-%H-%M-%S")
        logfilename = os.path.join(logDir,"log_" + ts_suffix + ".log")
        i=1
        while os.path.isfile(logfilename):
            logfilename = os.path.join(logDir,"log_" + ts_suffix + "_" + str(i) + ".log")
            i+=1

        os.rename(stdlogfilename,logfilename)

    currlogFilePath = os.path.join(logDir, stdlogfilename)
    f = open(currlogFilePath,"w+")
    return f

def destroy():
    logfile.close()
