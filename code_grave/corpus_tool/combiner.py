# encoding=utf-8
import time
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")

#print "Usage : python filter.py wrongfile < corpus > corpus.filter"
f1 = codecs.open(sys.argv[1],'r','utf-8').readlines()
f2 = codecs.open(sys.argv[2],'r','utf-8').readlines()

t1 = time.time()


run = 0

for index in range(0,len(f1)):
    run+=1
    sys.stdout.write(f1[index])
    sys.stdout.write(f2[index])

t2 = time.time()
tm_cost = t2-t1

#print('cost ' + str(tm_cost))
#print('speed %s lines/second' % (run/tm_cost))