# -*- coding:utf-8 -*-  
'''
   @Brief : Translates a source file using a translation model.
   @Modify: 2017/8/31 by revo (MARIAN version)
   @CopyRight: newtranx
'''
import os
import sys
import uuid
import random
import argparse

import json
import numpy
import codecs
import cPickle as pkl
import nmt_print_matrix

from util import load_dict
from util import load_config
from compat import fill_options
from hypgraph import HypGraphRenderer
from multiprocessing import Queue
from multiprocessing import Process



#------------------------------------------------------------------------------
#--@brief: Load model and new process do translate...
#--
#--@param: worker_ctx, ...
#--@param: sentence, ...
#--@param: saveto, ...
#--@param: save_alignment, ...
#--@param: k, ...
#--@param: normalize, ...
#--@param: n_process, ...
#--@param: chr_level, ...
#--@param: verbose, ...
#--@param: nbest, ...
#--@param: suppress_unk, ...
#--@param: a_json, ...
#--@param: print_word_probabilities, ...
#--@param: return_hyp_graph, ...
#--@param: logger, ...
#------------------------------------------------------------------------------
def instance( worker_ctx,
              sentence, 
              saveto,
              save_alignment= False,
              k             = 5,
              normalize     = False,
              n_process     = 5,
              chr_level     = False,
              verbose       = False,
              nbest         = False,
              suppress_unk  = False,
              a_json        = False,
              print_word_probabilities= False,
              return_hyp_graph        = False,
              logger                  = None
            ):
#-- begin->Func: translate --#
    #-- 每次一个会话id --#
    queue_idx = 0;
    queue_min_size = sys.maxint;
    for i in xrange( 0 , n_process) :
        if queue_min_size > worker_ctx['queue'][i].qsize() :
            queue_idx = i;
            queue_min_size = worker_ctx['queue'][i].qsize();
        
    session_id = str( uuid.uuid1());
    
    if logger is None:
        logger.info  = sys.stderr.write;
        logger.debug = sys.stderr.write;
        logger.error = sys.stderr.write;

    #-- The _seqs2words inside function --#
    def _seqs2words( cc):
        ww = []
        for w in cc:
            if w == 0:
                break;
            else :
                ww.append( worker_ctx['word_idict_trg'][ w]);
        return ' '.join( ww);
    #-- end->Func: _seqs2words --#


    #-- The _send_jobs inside function --#
    def _send_jobs( f):
        source_sentences = []
        for idx, line in enumerate( f):
            if chr_level:
                words = list( line.decode('utf-8').strip());
            else:
                #-- split line to words with default --#
                words = line.strip().split();
            #-- All words append into x list --#
            x = [];
            '''for w in words:
                w = [ worker_ctx['word_dicts'][i][f] if f in worker_ctx['word_dicts'][i] else 1 for (i,f) in enumerate( w.split('|'))];
                if len( w) != worker_ctx['options'][0]['factors']:
                    #-- Dump error log --#
                    logger.error( 'Error: expected {0} factors, but input word has {1}\n'.format(worker_ctx['options'][0]['factors'], len( w)));
                    for midx in xrange(n_process):
                        #-- Terminate all processes --#
                        #processes[midx].terminate();
                        pass;
                    #sys.exit(1);
                #-- append w to x list --#
                x.append( w);
            '''
            #x += [[0]*worker_ctx['options'][0]['factors']];
            x = [line.strip()]
            #-- Put (idx, x) input worker_ctx['queue'] --#
            try :
                worker_ctx['req_lock'][queue_idx].acquire();
                worker_ctx['queue'][queue_idx].put([ idx, x, session_id]);
                worker_ctx['resp_lock'][queue_idx].acquire();
                worker_ctx['req_lock'][queue_idx].release();
                logger.info( "<Start>: session.{} --> Put request data to queue ok.".format( session_id));
                logger.info( "<Queue>: queue size.{0}".format( worker_ctx['queue'][queue_idx].qsize()));
            except :
                worker_ctx['resp_lock'][queue_idx].release();
                worker_ctx['req_lock'][queue_idx].release();
                logger.error( "<Error>: Put request to queue failed.");

            #-- Append words into source_sentences --#
            source_sentences.append( words);
        return idx+1, source_sentences;
    #-- end->Func: _send_jobs --#
    

    #-- The _retrieve_jobs function --#
    def _retrieve_jobs( n_samples):
        out_idx = 0;
        trans   = [None] * n_samples;

        for idx in xrange( n_samples):
            while True :
                try :
                    resp = worker_ctx['rqueue'][queue_idx].get( True, 20);
                    if resp is not None :
                        logger.info( "<End>: Get response data from queue ok.");
                        #-- 对比session --#
                        if session_id == resp[ 2] :
                            worker_ctx['resp_lock'][queue_idx].release();

                            trans[ resp[0] ] = resp[1];
                            if verbose and numpy.mod(idx, 10) == 0:
                                #-- Dump info message logger --#
                                logger.info( 'Sample {0} / {1} Done'.format( ( idx+1), n_samples));

                            while out_idx < n_samples and trans[ out_idx] != None:
                                yield trans[ out_idx];

                                out_idx += 1;

                            #-- 推出while True --#
                            logger.info( "<Response>: session.{} <-- Get response data from queue ok.".format( session_id));

                            break;
                        else :
                            #-- 脏数据清理，如果100次都没有用就清除 --#
                            if 64 > resp[3] :
                                resp[3] = resp[3] + 1;
                                #-- 不是自己的不能拿 --#
                                try :
                                    worker_ctx['rqueue'][queue_idx].put( resp);
                                except :
                                    pass;
                    else :
                        worker_ctx['resp_lock'][queue_idx].release();
                        logger.error( "Error: Get response from queue which nothing data...");

                        break;
                except Exception, e:
                    worker_ctx['resp_lock'][queue_idx].release();
                    logger.error( "Error: Get response from queue timeout...: %s" % e);

                    break;
    #-- end-    >Func: _retrieve_jobs --#

    
    #-- Log dump -->
    logger.info( 'nmt_translate: translating sentence.<%s> ...' % (sentence));

    n_samples, source_sentences = _send_jobs( [sentence.encode('utf-8')]);

    result        = "";
    alignmentInfo = "";

    for i, trans in enumerate( _retrieve_jobs( n_samples)):

        #-- Get samples, scores, word_probs, alignment, hyp_graph --#
        #samples, scores, word_probs, alignment, hyp_graph = trans;

        #-- seqs to words from samples --#
        #result += _seqs2words( samples);
        #if print_word_probabilities:
        #    for prob in word_probs:
        #        result += "{} ".format( prob);
        result = trans;

    # sys.stderr.write('Done\n');
    result_ALL = dict();
    result_ALL['translation'] = result;
    result_ALL['alignment']   = False;
    result_ALL['align']       = None;

    return result_ALL;
#-- end->Func: translate --#



