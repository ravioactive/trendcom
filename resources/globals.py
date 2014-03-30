# -*- coding: utf-8 -*-
import re
import os
import pymongo
import time
import datetime

def init():

    global x_consumer_key
    x_consumer_key = "cYyGL0vbIRWMiTAJ9rcQ8A"
    global x_consumer_secret
    x_consumer_secret = "HVWH8oe5ut6hpoD5HbkKVtBU0StYuBVezbg0iIHklpc"
    global x_access_token
    x_access_token = "51518286-uSn7aIdVPSfQBk6uWexPqdU8cx6SPTMrNLvlo1tpC"
    global x_access_token_secret
    x_access_token_secret = "e2AKBACbYgUvaVZOcAnv5wlxEKjsl3wfR1PfE7uXLuvFt"

    global t_consumer_key
    t_consumer_key = "wgCW9kuShXD8Ck9oPibLhw"
    global t_consumer_secret
    t_consumer_secret = "YK7dvpmpXvqkEtzBPD2R3cpWZOPgtiFtAlg3uifHU"
    global t_access_token
    t_access_token = "51518286-kVybQaBS0hKzcJaZA5fVk39bHTnMkqVeXuyF2qvUB"
    global t_access_token_secret
    t_access_token_secret = "H8RNy01CpIEcBhn9wqTek2YEOjYtaVkiYirirK2s6YBCl"

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
    ts_suffix = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d-%H-%M-%S")
    logfilename = "log_" + ts_suffix + ".log"
    logFilePath = os.path.join(os.path.join(os.path.join(os.path.abspath(os.path.pardir),'code'),'logs'),logfilename)
    f = open(logFilePath,"w+")
    return f

def destroy():
    logfile.close()
