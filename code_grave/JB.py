# encoding=utf-8
import time
import sys
#sys.path.append("../")
import jieba
import codecs
#jieba.initialize()

In = sys.argv[1]
output = sys.argv[2]
lines =  codecs.open(In,'r','utf-8')

#content = open(url,"rb").read()
t1 = time.time()

words = []
#print jieba.cut("HIHI")
run = 0
log_f = codecs.open(output,"wb",'utf-8')
for line in lines:
    run += 1
    #words.append( " ".join(jieba.cut(line,cut_all=False)))
    
    log_f.write(" ".join(jieba.cut(line,cut_all=False)))
    #print " ".join(jieba.cut(line,cut_all=False))

t2 = time.time()
tm_cost = t2-t1


log_f.close()

print('cost ' + str(tm_cost))
print('speed %s lines/second' % (run/tm_cost))

