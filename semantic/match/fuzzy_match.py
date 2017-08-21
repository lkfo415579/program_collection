import sys
import pickle
#import aspell
from collections import Counter, defaultdict
import operator    
import nltk
from nltk.corpus import stopwords
import re
import jellyfish


def preprocess(input_str, normalized = True, ignore_list = []):
    for ignore_str in ignore_list: 
        input_str = re.sub(r'{0}'.format(ignore_str), "", input_str, flags=re.IGNORECASE)
    if normalized is True:
        input_str = input_str.strip().lower()
        input_str = re.sub("\W", "", input_str).strip()
    return input_str





def find_string_similarity(first_str, second_str):
    match_score = jellyfish.jaro_winkler(unicode(first_str), unicode(second_str))
    return match_score
    
        
    

def matching(query, bucket, normalized = True, ignore_list= []):
    query  = preprocess(query, normalized = normalized, ignore_list = ignore_list)
    q_len = len(query)

    list_ = bucket[q_len - 2]+bucket[q_len - 1] + bucket[q_len] + bucket[q_len+1]+bucket[q_len + 2]
    score_list = []
    for i in range(len(list_)):
        score_list.append(find_string_similarity(query, list_[i]))
    index, value =    max(enumerate(score_list), key = operator.itemgetter(1))
    if value > 0.8:
        return list_[index]
    return None
        
def query_process(query_string,bucket,dic):
    
    query_words = query_string.strip().split()
    query_word_list =[w for w in query_words if w not in stopwords.words('english') ] 
    query_entity = ' '.join(word for word in query_word_list) 
    entity_disease = matching(query_entity, bucket, normalized = True, ignore_list = [])
    if entity_disease == None:
        print query_entity + " is no found!"
        return False
        
    
    CUI = dic[entity_disease]
    #print dic
    return query_entity,CUI


def main():
    query_string = sys.argv[1]
    print query_process(query_string)
if __name__ == "__main__":
    main()

    
