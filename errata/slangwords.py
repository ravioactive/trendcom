from __future__ import print_function
import os
import re

def main():
    project_dir=os.path.join(os.path.join(os.path.abspath(os.path.pardir),'resources'),'slangwords')

    slangword_files_regex=r'slang[\w\d].txt'
    slangwordfiles=[]
    root,blah,allfiles=os.walk(project_dir,True,None,False).next()
    slangwordfiles=[match.group() for filename in allfiles for match in [re.search(slangword_files_regex,filename)] if match]
    print(slangwordfiles)

    allslangwords_set=set()
    for sw_fn in slangwordfiles:
        #print(sw_fn)
        with open(os.path.join(root,sw_fn),'r') as swf:
            for slangword in swf:
                #print(slangword)
                if slangword not in allslangwords_set:
                    allslangwords_set.add(slangword)

    print('set size:', len(allslangwords_set))

    with open(os.path.join(root,'all_slangwords.txt'),'w') as all_slang_words_file:
        all_slang_words_file.truncate()
        for sw in allslangwords_set:
            #print(sw,end="")
            #print(re.sub('[^A-Za-z0-9]+','',sw),end=",",file=all_stop_words_file)
            print(sw,end='',file=all_slang_words_file)


if __name__ == '__main__':
    main()
