# encoding=utf-8
import json
import time
import sys
#import codecs
import pickle
import networkx as nx
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
import numpy as np

#import pygraphviz
#from networkx.draw.G.nx_agraph import graphviz_layout

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
#plt.ioff()
import match.fuzzy_match as fuzzy

def print_network(network,network_keys,N):
    tmp = 0
    for node in network_keys:
        print node
        print network[node]
        tmp +=1
        if tmp > N:
            break
    
class SNetwork:
    def __init__(self, network_path):
        #self.query = query
        self.network = pickle.load(open(network_path, "r"))
        network_keys = sorted(self.network)
        print_network(self.network,network_keys,1)
        self.G = nx.Graph()
        self.t1 = time.time()
        #add nodes and name, and edge
        print "Length of Network: %d" % len(self.network)
        print "Staring construct the network"
        self.construct(network_keys)
        
        #PageRANK_TMP
        try:
            self.PageRANK = pickle.load(open("PageRANK.p", "r"))
        except:
            self.PageRANK = {}
        
        #import fuzzy matching
        
        self.bucket = pickle.load(open('match/bucket.p','rb'))
        self.dic = pickle.load(open('match/dic.p','rb'))
        
    def construct(self,network_keys):
        global run
        run=0
        edges = 0
        for node in network_keys:
            run+=1
            if run % 100 == 0:
                sys.stdout.write("\rRunning:%d" % run)
                sys.stdout.flush()
            try:
                if self.G.node[node]:
                    continue
            except:
                self.G.add_node(node, Name=self.network[node]['Name'])
                
            for REL in self.network[node]['Relation']:
                #for testing
                try:
                    if self.G.node[REL]:
                        pass
                except:
                    self.G.add_node(REL, Name=self.network[REL]['Name'])
                self.G.add_edge(node, REL, weight=1)
                edges+=1
            #if run >= 10:
            #    break
        print "\rAmount of Nodes: %d" % self.G.number_of_nodes()
        print "Amount of Edges: %d" % self.G.number_of_edges()
    def query(self,query):
        #############
        #Get specific node
        NODELIST = []
        EDGES_LIST = []
        HEAD_NODE = None
        NODES_DATA = {}
        T = nx.Graph()

        #query = sys.argv[2]
        print "Your query : %s" % query
        query = query.lower()
        for node in self.G.nodes():
            #if len(self.G.neighbors(node)) > 10:
            #    print self.G.node[node]['Name']
            #print self.G.node[node]['Name']
            #if self.G.node[node]['Name'] == "HIV":
            if self.G.node[node]['Name'].lower() == query:
                NODELIST.append(node)
                NODELIST+=self.G.neighbors(node) 
                EDGES_LIST = self.G.edges(node)
                #ADD head node
                HEAD_NODE = node
                
                #
                for N in NODELIST:
                    ##ADD data
                    #remove relation keys
                    self.network[N].pop("Relation",None)
                    NODES_DATA[N] = self.network[N]
                    ###
                    T.add_node(N, Name=self.network[N]['Name'])
                T.add_edges_from(EDGES_LIST)
                break
        
        #FUZZY_MATCHED = False
        if len(NODELIST) == 0 :
            #can't match
            try:
                fuzzy_result = fuzzy.query_process(query,self.bucket,self.dic)
                if (fuzzy_result):
                    #FUZZY_MATCHED = True
                    print "###MATCHED FUZZY####"
                    return self.query(self.G.node[fuzzy_result[1]]['Name'])
            except:
                pass
                #error
                
                
                
        ####

        #print NODELIST
        #print EDGES_LIST

        labels = {}
        for node in NODELIST:
            labels[node] = T.node[node]['Name']

            
        #JSON = json.dumps({"NODELIST":NODELIST,"HEAD_NODE":HEAD_NODE,"EDGES_LIST":EDGES_LIST,"NODES_DATA":NODES_DATA})
        Result = {"NODELIST":NODELIST,"HEAD_NODE":HEAD_NODE,"EDGES_LIST":EDGES_LIST,"NODES_DATA":NODES_DATA}
        
        #
        #G = nx.lollipop_graph(4, 3)
        #G=nx.cycle_graph(24)
        #pos=nx.spring_layout(G,iterations=200)
        ##
        #nx.draw(G)
        #nx.draw_random(G)
        #pos=nx.circular_layout(G,scale=1.0)
        #pos=nx.shell_layout(G,scale=1.0)
        #pos=nx.spectral_layout(G,scale=1.0)
        #pos=nx.random_layout(G)
        #pos = graphviz_layout(G, prog='twopi', args='')
        #print pos
        #colors=range(len(self.network))
        #colors=range(edges-1)
        #print self.G.nodes()
        #print self.G.edges()
        #sys.exit()
        ################################
        #pos=nx.spring_layout(T,iterations=50,k=150)
        #################
        #colors="#000000"
        #colors=range(self.G.number_of_edges())
        #NODE_COLOR = range(self.G.number_of_nodes())
        
        #NODE_COLOR = "#00ff80"
        #colors=range(len(EDGES_LIST))
        #nx.draw_networkx(T,pos,node_size=800,labels=labels,nodelist=NODELIST,edgelist=EDGES_LIST,node_color=NODE_COLOR,font_size='10',edge_color=colors,width=2,edge_cmap=plt.cm.Blues)


        #plt.axis('off')
        #plt.savefig("edge_colormap.png",dpi=150)

        ###
        t2 = time.time()
        print "End of Construct network"

        tm_cost = t2-self.t1
        global run
        print('cost %s s ' % str(tm_cost))
        print('speed %f operation/second' % (run/tm_cost))
        
        #return JSON
        return Result
    def check_surround_node(self,name,pr):
        pro = {}
        NODES_LIST = []
        NODES_PRO = []
        name = name.lower()
        for node in self.G.nodes():
            if self.G.node[node]['Name'].lower() == name:
                #print pr[node]
                for neighbor in self.G.neighbors(node):
                    print self.G.node[neighbor]['Name']," ## ",self.network[neighbor]['Type']," @@ ",neighbor
                    print pr[neighbor]*1000
                    #insert pro
                    NODES_LIST.append(neighbor)
                    NODES_PRO.append(pr[neighbor]*1000)
        #there is no relations
        if len(NODES_PRO) == 0:
            return {}
        NODES_PRO = self.softmax(NODES_PRO)
        print NODES_PRO
        pro =  {NODES_LIST[x]:NODES_PRO[x] for x in range(0,len(NODES_LIST))}
        #print pro
        return pro
    def softmax(self,x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0) # only difference
    def recursive(self,node,personalization,running):
        if running == 0.0:
            #print "Reached end"
            #return personalization
            return
        for neighbor in self.G.neighbors(node):
            self.P.add_edge(node, neighbor, weight=1)
            #personalization[neighbor] = round((running/10)*3,1)
            personalization[neighbor] = round((running/self.Depth),1)
            self.recursive(neighbor,personalization,running-1)

    def page_rank(self,query,depth=5.0):
        print "Computing PageRANK"
        
        print "Your query : %s" % query
        print "Depth : %s" % depth
        personalization = {}
        query = query.lower()
        self.P = nx.Graph()
        self.Depth = depth
        for node in self.G.nodes():
            if self.G.node[node]['Name'].lower() == query:
                personalization[node] = 1
                #HEAD NODE
                self.P.add_node(node)
                self.recursive(node,personalization,self.Depth)
                #print personalization
                #print self.P.nodes()
                break
                #for neighbor in self.G.neighbors(node):
                #    personalization[neighbor] = 0.6
            #else:
            #    personalization[node] = 0
        #personalization={1:1, 2:1, 3:1, 4:1}
        try:
            pr = nx.pagerank(self.P,personalization=personalization, alpha=0.9)
        except:
            return {}
        return self.check_surround_node(query,pr)
        #print pr
    def construct_page_rank(self,depth=5.0):
        t0 = time.time()
        print "Constructing PageRANK"
        for node in self.G.nodes():
            self.PageRANK[node] = self.page_rank(self.G.node[node]['Name'],depth)
            #break
        print "Finished PageRANK"
        t1 = time.time()
        print "Costed : %f" % (t1-t0)
        pickle.dump(self.PageRANK,open('PageRANK.p','w'))

            
    def write_entity(self,key,output,k):
        f = open(output,"wa")
        for node in self.G.nodes():
            if self.network[node]['Type'][:3] == "Dis":
                if len(self.G.edges(node)) > k:
                    f.write(self.G.node[node][key]+"\n")
            
        f.close()
    def get_page_rank(self,query,sort=True):
        print "Searching PageRANK"
        for node in self.G.nodes():
            if self.G.node[node]['Name'].lower() == query:
                #print self.PageRANK[node]
                pro = self.PageRANK[node]
                break
                
        if sort:
            dic_sort = sorted(pro.items(),key=lambda pro:pro[1],reverse=True)
            pro = dic_sort
            #print dic_sort
            #pro2 = {}
            #for item in dic_sort:
            #    pro2[item[0]] = item[1]
            #print json.dumps(dic_sort)
            #pro2 = dict(dic_sort)
            #print pro
        #print "PRO2"
        #print pro2
        try:
            return pro
        except:
            return {}
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print "Usage: [network.p]"
        sys.exit()
    SNet = SNetwork(sys.argv[1])
    #SNet.get_page_rank(sys.argv[2].lower())
    #print SNet.query(sys.argv[2])
    #SNet.page_rank(sys.argv[2])
    #SNet.write_entity("Name","tmp_NAME",20)
    #SNet.construct_page_rank()
