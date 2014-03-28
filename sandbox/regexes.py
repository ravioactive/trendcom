# -*- coding: utf-8 -*-

import re

def matchGt2(string):
    #res = pat.match(string)
    # if res:
    #     print 'shit found'
    #     i=0
    #     while res.group(i):
    #         print res.group(i)
    #         i+=1
    #     #print res.group(1)
    # else:
    #     print 'nothing'
    pat = re.compile(r"(.)\1{2,}", re.DOTALL)
    res = re.sub(pat,r"\1\1",string)
    #res = pat.findall(string)
    print len(res), string, res

def matchPunctGt2(tweet):
    print tweet, "."
    tweet=re.sub('[^a-zA-Z0-9]+',' ',tweet)
    # print tweet
    # tweet = re.sub('[\s]+', ' ', tweet)
    print tweet+"."
    print tweet.strip()+"."

def every_url(urls):
    urlpat=re.compile(r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
    for url in urls:
        res = urlpat.findall(url)
        print len(res), "\nGIVEN:", url, "\nFOUND:", res[0][0] if res else ''
        res2 = re.sub(urlpat,'',url)
        print 'SUBS:', res2


if __name__ == '__main__':
    #print "[^\s`!()\[\]{};:'\".,<>?«»“”‘’]"
    #matchPunctGt2("        aa    sds  ewrw          ")
    every_url(["asdasdas","http://daringfireball.net/2010/07/improved_regex_for_matching_urls","http://goo.gl/qwIwus","http://goo.gl/Y95sdJ","http://tcrn.ch/1rH7Fkx  by @alex","pic.twitter.com/3dE4SFgUmT","bit.ly/foo","is.gd/foo/","1. amazing fit  @TBdressClub dress=>http://goo.gl/qwIwus        shoes=>htt"])
