# encoding=utf-8
import time
import sys
import codecs
import re, mmap
import uniout
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

if (len(sys.argv) < 3):
    print "Usage: [MRSTY.RRF][T037]"
    sys.exit()
In = sys.argv[1]
T = sys.argv[2]

f =  codecs.open(In,'r','utf-8')
STY_LINES = f.readlines()

t1 = time.time()

run = 0

OUTPUT = codecs.open('STY_OUT',"wa",'utf-8')
for x in range(0,len(STY_LINES)):
    run+=1
    ######
    if x % 1000 == 0:
        sys.stdout.write("\rHEY:%d" % x)
        sys.stdout.flush()
    #######
    entity = STY_LINES[x].split("|")
    if (entity[1] == T):
        OUTPUT.write(STY_LINES[x])
    


t2 = time.time()
tm_cost = t2-t1

OUTPUT.close()
f.close()

print('cost ' + str(tm_cost))
print('speed %s lines/second' % (run/tm_cost))


