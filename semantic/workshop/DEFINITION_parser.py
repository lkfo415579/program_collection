# encoding=utf-8
import time
import sys
import codecs
#import re, mmap
#import uniout
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

if (len(sys.argv) < 3):
    print "Usage: [STY_OUT][CUI][MRREL.RRF]"
    sys.exit()
In = sys.argv[1]
TYPE = sys.argv[2]
LIB = "MRREL.RRF"

f =  codecs.open(In,'r','utf-8')
STY_LINES = f.readlines()


with codecs.open(LIB,'r+','utf-8') as f2:
    data = f2.readlines()

saver = 0
t1 = time.time()
run = 0
def EXACT_search(Search_CUI):
    #phrase = Search_CUI+r"||"+TYPE+r".*$"
    phrase = Search_CUI+"||"+TYPE
    global saver
    global data
    #data2 = data[saver:]
    result = []
    for x in range(saver,len(data)):
        #mo = re.search(phrase, data2[x])
        if data[x][:len(phrase)] == phrase:
            content = data[x]
            saver = x
            #print "GOT"
            #print content
            result.append(content)
            #mo = None
            #saver = x
        
        if int(data[x][1:8]) > int(Search_CUI[1:8]):
            #print int(data[x][1:8])," ",int(Search_CUI[1:8])
            break
    
    try:
        return result
    except:
        return False

OUTPUT = codecs.open('RELATION_OUT',"wa",'utf-8')
for x in range(0,len(STY_LINES)):
    run+=1
    ######
    if x % 10 == 0:
        sys.stdout.write("\rXDXD:%d" % x)
        sys.stdout.flush()
    #######
    entity = STY_LINES[x].split("|")
    Search_CUI = entity[0]
    return_LINE = EXACT_search(Search_CUI)
    
    if return_LINE:
        for line in return_LINE:
            line = line.replace("||","|").split("|")
            sys.stdout.write("\r            Runner:%s" % line[0])
            OUTPUT.write(line[0]+"|"+line[3]+'\n')
    


t2 = time.time()
tm_cost = t2-t1

OUTPUT.close()
f.close()

print('cost ' + str(tm_cost))
print('speed %s lines/second' % (run/tm_cost))


