# -*- coding: utf-8 -*-
import re
import os

def init():
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

def getAllStopwords():
    allStopWordsFile=os.path.join(os.path.join(os.path.join(os.path.join(os.path.abspath(os.path.pardir),'code'),'resources'),'stopwords'),'all_stopwords.txt')
    return open(allStopWordsFile,'r').read().splitlines()

def getSlangDictionary():
    allSlangWordsFile=os.path.join(os.path.join(os.path.join(os.path.join(os.path.abspath(os.path.pardir),'code'),'resources'),'slangwords'),'all_slangwords.txt')
    return {k:v for (k,v) in [slw.split(':') for slw in open(allSlangWordsFile,'r')]}
