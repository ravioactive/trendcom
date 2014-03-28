from __future__ import print_function
import os
import re

def main():
    project_dir=os.path.join(os.path.join(os.path.abspath(os.path.pardir),'resources'),'stopwords')
    stopword_files_regex=r'stopwords[\d]+\.txt'
    stopwordfiles=[]
    root,blah,allfiles=os.walk(project_dir,True,None,False).next()
    stopwordfiles=[match.group() for filename in allfiles for match in [re.search(stopword_files_regex,filename)] if match]
    print(stopwordfiles)

    allstopwords_set=set()
    for sw_fn in stopwordfiles:
        #print(sw_fn)
        with open(os.path.join(root,sw_fn),'r') as swf:
            for stopword in swf:
                #print(stopword)
                if stopword not in allstopwords_set:
                    allstopwords_set.add(stopword)

    print('set size:', len(allstopwords_set))

    with open(os.path.join(root,'all_stopwords.txt'),'w') as all_stop_words_file:
        all_stop_words_file.truncate()
        for sw in allstopwords_set:
            #print(sw,end="")
            #print(re.sub('[^A-Za-z0-9]+','',sw),end=",",file=all_stop_words_file)
            print(sw,end='',file=all_stop_words_file)


if __name__ == '__main__':
    main()
