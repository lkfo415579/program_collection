# -*- coding:utf-8 -*-  
'''
   @Brief : Translates a source file using a translation model.
   @Modify: 2017/8/31 by revo (MARIAN version)
   @CopyRight: newtranx
'''
import os
import sys
import time
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

import marian_python.libamunmt as nmt

def _set_device(device_id,logger):
    """
    Modifies environment variable to change the THEANO device.
    """
    if device_id != '':
        try:
            theano_flags = os.environ['THEANO_FLAGS'].split(',')
            exist = False
            for i in xrange(len(theano_flags)):
                if theano_flags[i].strip().startswith('device'):
                    exist = True
                    theano_flags[i] = '%s=%s' % ('device', device_id)
                    break
            if exist is False:
                theano_flags.append('%s=%s' % ('device', device_id))
            os.environ['THEANO_FLAGS'] = ','.join(theano_flags)
        except KeyError:
            # environment variable does not exist at all
            os.environ['THEANO_FLAGS'] = 'device=%s' % device_id
        logger.info("ENVIR:{0}".format(os.environ['THEANO_FLAGS']))



#-- 翻译模型 --#
def translate_model( queue,     \
                     rqueue,    \
                     pid,       \
                     models,    \
                     options,   \
                     k,         \
                     normalize, \
                     verbose,   \
                     nbest,     \
                     return_alignment, \
                     suppress_unk,     \
                     return_hyp_graph, \
                     mutex, \
                     logger, \
                     device_id
                   ):
#-- Begin->Func: translate_model -->
    from nmt import build_sampler
    from nmt import gen_sample
    from nmt import init_params
    from theano      import shared
    from theano_util import (numpy_floatX, load_params, init_theano_params)
    from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams

    #ADD by revo
    logger.debug("Process '%s' - Loading models on GPU %s\n" % (pid, device_id))
    # modify environment flag 'device'
    #_set_device(device_id,logger)
    ##########
    config = ['-c', 'marian_python/GPU.0']
    nmt.init(" ".join(config))
  

    #-- _translate function --#
    def _translate(seq):
        logger.debug("NMT seq %s" % seq)
        trans = nmt.translate_single(seq)[0]
        logger.debug("NMT trans %s" % trans)
        return nmt.translate_single(seq)[0]
        #return sample[sidx], score[ sidx], word_probs[ sidx], alignment[sidx], hyp_graph;
        #return nmt.translate_single(sentences)[0],666,None,None,None

    #-- Loop get data from input queue and call _translate --#
    while True:
        req = None;
        try :
            req = queue.get()
        except :
            req = None;
        
        if req is None:
            #-- None data from request queue --#
            break;
        else :
            idx, x, session_id = req[0], req[1], req[2];
            if verbose:
                #-- record pid and idx to stderr --#
                sys.stderr.write('{0} - {1}\n'.format( pid, idx));

            try :
                #-- Do translate and get result --#
                start_time = time.time();
                seq = _translate(x);
                end_time = time.time();
                logger.info( "<-End->: translate.data.size.{} -- time.{}".format( len( x), (end_time - start_time)) );

                #-- Put result to respose queue --#
                rqueue.put([ idx, seq, session_id, 0]);
            except :
                pass;

    return;
#-- end->Func: translate_model --#


#------------------------------------------------------------------------------
#--@brief: Load model and new process do translate...
#--
#--@param: worker_ctx, ...
#--@param: models, ...
#--@param: source_file, ...
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
#--@param: pidfile
#------------------------------------------------------------------------------
def instance( worker_ctx,
              models,
              source_file,
              saveto,
              #save_alignment= True,
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
              logger        = None,
              pidfile       = None,
              devices_list = None
            ):
    #-- load model model_options --#
    for model in models:
        worker_ctx['options'].append(load_config(model));

        fill_options( worker_ctx[ 'options'][ -1]);

    dictionaries = worker_ctx['options'][0]['dictionaries'];
    dictionaries_source = dictionaries[ : -1];
    dictionary_target   = dictionaries[ -1  ];
    ####################BY_REVO###############
    # load and invert source dictionaries
    word_dicts = []
    word_idicts = []
    for dictionary in dictionaries_source:
        word_dict = load_dict(dictionary)
        if worker_ctx['options'][0]['n_words_src']:
            for key, idx in word_dict.items():
                if idx >= worker_ctx['options'][0]['n_words_src']:
                    del word_dict[key]
        word_idict = dict()
        for kk, vv in word_dict.iteritems():
            word_idict[vv] = kk
        word_idict[0] = '<eos>'
        word_idict[1] = 'UNK'
        word_dicts.append(word_dict)
        word_idicts.append(word_idict)

    worker_ctx['word_dicts'] = word_dicts
    worker_ctx['word_idicts'] = word_idicts

    # load and invert target dictionary
    word_dict_trg = load_dict(dictionary_target)
    word_idict_trg = dict()
    for kk, vv in word_dict_trg.iteritems():
        worker_ctx['word_idict_trg'][vv] = kk
    worker_ctx['word_idict_trg'][0] = '<eos>'
    worker_ctx['word_idict_trg'][1] = 'UNK'
    
    #$#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    #-- create input and output queues for processes --#
    processes = [None] * n_process;
    for midx in xrange(  n_process):
        #Device ID
        device_id = devices_list[midx % len(devices_list)]
        #-- 放弃对队列枷锁，免得进程挂过后请求和响应牛头不对马嘴 --#
        logger.info( 'Create nmt subprocess.<{}>...'.format( midx));
        
        _set_device(device_id,logger)
        
        processes[ midx] = Process( target=translate_model, \
                                    args  =(worker_ctx['queue' ][midx], \
                                            worker_ctx['rqueue'][midx], \
                                            midx,                 \
                                            models,               \
                                            worker_ctx['options'],\
                                            k,                    \
                                            normalize,            \
                                            verbose,              \
                                            nbest,                \
                                            save_alignment,       \
                                            suppress_unk,         \
                                            return_hyp_graph,     \
                                            worker_ctx['lock'],   \
                                            logger,
                                            device_id\
                                          ) \
                                  );

        #-- Start a subprocess --#
        processes[ midx].start();
        logger.info( 'Create nmt subprocess.<{}> pid.<{}> is running ok.'.format( midx, processes[ midx].pid));
        logger.info( 'Specify queue.<{}> rqueue<{}>.'.format( str( worker_ctx['queue'][ midx]), str( worker_ctx['rqueue'][ midx])));

        #-- Save the translate process id to file --#
        try:
            file_pid = open( pidfile, 'w');
            try:
                file_pid.write( str( processes[ midx].pid) + "\n");
            except:
                pass;
            #-- Must close file --#
            file_pid.close();
        except:
            pass;

    return processes;
#-- end->Func: instence --#


