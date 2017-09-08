# encoding=utf-8
import time
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")

#print "Usage : python filter.py wrongfile < corpus > corpus.filter"
wrong = codecs.open(sys.argv[1],'r','utf-8')

t1 = time.time()


run = 0
line_num=[]
corpus = sys.stdin.readlines()
for line in wrong.readlines():
    run += 1
    #print "HEY"
    #print line
    #print line.split("|||")[0]
    try:
        corpus[int(line.split("|||")[0])] = "@@@@"
    except:
        pass
#print "Processing. . . . . ."
for index,line in enumerate(corpus):
    run+=1
    if line is not "@@@@":
        sys.stdout.write(line)
    

t2 = time.time()
tm_cost = t2-t1

#print('cost ' + str(tm_cost))
#print('speed %s lines/second' % (run/tm_cost))