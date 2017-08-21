# encoding=utf-8
import time
import sys
import codecs
import pickle
#import re, mmap
#import uniout
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def print_network(network,network_keys):
    tmp = 0
    for node in network_keys:
        print node
        print network[node]
        tmp +=1
        if tmp > 10:
            break


if (len(sys.argv) < 2):
    print "Usage: [RELATION_OUT]"
    sys.exit()
In = sys.argv[1]
#Position = sys.argv[2]
LIB = "MRCONSO.RRF"
LIB2 = "MRDEF.RRF"
LIB3 = "MRSTY.RRF"

f =  codecs.open(In,'r','utf-8')
STY_LINES = f.readlines()


with codecs.open(LIB,'r+','utf-8') as f2:
    CONSO = f2.readlines()
with codecs.open(LIB2,'r+','utf-8') as f2:
    DEF = f2.readlines()
with codecs.open(LIB3,'r+','utf-8') as f2:
    STY = f2.readlines()
    
saver = 0
t1 = time.time()
run = 0
def EXACT_search(Search_CUI,phrase,data,step):
    phrase = Search_CUI+phrase
    global saver
    #sys.stdout.write("\r                 SAVER:%d" % saver)
    
    #step = 100
    tmp_step = 0
    error = 0
    x = saver
    final_sign = 0
    while x < len(data):
        #print int(data[x][1:8]), " " , int(Search_CUI[1:]), " " , tmp_step
        #print Search_CUI
        #print data[x][1:8].isdigit()
        #print data[x]
        #print "@%d"%x
        if int(data[x][1:8]) > int(Search_CUI[1:]):
            x=max(1,x - (step+1))
            #print "SS:%d" % x
            #sys.exit()
            if tmp_step == 1:
            #    #can't find in the DATABASE
                 final_sign +=1
                 if final_sign > step+5:
                    break
            #    break
            continue
        
        #print phrase," ",data[x]
        #print data[x]
        if phrase in data[x]:
            #result = data[x].replace("||","|").split("|")
            result = data[x].split("|")
            saver = x
            #print saver
            #print result
            break
        else:
            tmp_step = max(1,step - error*10)
            x+=tmp_step
            error+=1
        
        

    
    try:
        return result
    except:
        #print Search_CUI
        return False

network = dict()
print "Starting building initi dict"
for x in range(0,len(STY_LINES)):
    run+=1
    ######
    if x % 100 == 0:
        sys.stdout.write("\rXDXD:%d" % x)
        sys.stdout.flush()
    #######
    entity = STY_LINES[x].split("|")
    entity[1] = entity[1].strip()
    if not (entity[0] in network):
        network[entity[0]] = {"Name":"","Definition":"","Relation":[entity[1]]}
    else:
        network[entity[0]]["Relation"].append(entity[1])
    ##The connected node also insert into dict
    if not (entity[1] in network):
        network[entity[1]] = {"Name":"","Definition":"","Relation":[]}
    
    
print "\nEnd of building initi dict"
print "Length of Network: %d" % len(network)
network_keys = sorted(network)
#print type(network)

#####
saver = 0
x = 0
print "Start of Inesrting name into dict"
for node in network_keys:
    x+=1
    if x % 100 == 0:
        sys.stdout.write("\rNAME:%d" % x)
        sys.stdout.flush()
        #print_network(network,network_keys)
    entity = EXACT_search(node,"|ENG|P|",CONSO,150)
    NAME = entity[-5]
    network[node]['Name'] = NAME
    #sys.exit()
print "End of Inesrting name into dict"

####
saver = 0
x = 0
print "Start of Inesrting Definition into dict"
for node in network_keys:
    x+=1
    if x % 100 == 0:
        sys.stdout.write("\rDEF:%d" % x)
        sys.stdout.flush()
        #print_network(network,network_keys)
    entity = EXACT_search(node,"|",DEF,50)
    if entity:
        DEF_DATA = entity[-4]
        network[node]['Definition'] = DEF_DATA
    #sys.exit()
print "End of Inesrting Definition into dict"

####
saver = 0
x = 0
print "Start of Inesrting STY into dict"
for node in network_keys:
    x+=1
    if x % 100 == 0:
        sys.stdout.write("\rSTY:%d" % x)
        sys.stdout.flush()
        #print_network(network,network_keys)
    entity = EXACT_search(node,"|",STY,50)
    if entity:
        TYPE = entity[-4]
        network[node]['Type'] = TYPE
    #sys.exit()
print "End of Inesrting STY into dict"
##


print_network(network,network_keys)
pickle.dump(network,open('Network.p','w'))


t2 = time.time()
tm_cost = t2-t1

f.close()

print('cost ' + str(tm_cost))
print('speed %s lines/second' % (run/tm_cost))


