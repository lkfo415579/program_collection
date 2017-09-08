#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
   @Brief : Translates a source file using a translation model.
   @Modify: 2017/8/31 by revo (MARIAN version)
   @CopyRight: newtranx
'''
import os
import sys
import time

from threading import Lock
from multiprocessing import Queue
from multiprocessing import Process

import nmt_load_model



#-------------------------------------------------------------------------------
#--@brief: Monitor all subprocess, if die of one, and then to restart it...
#--
#--@param: process_pool, All subprocess handler list...
#--
#--@return: None...
#-------------------------------------------------------------------------------
def instance( server_ctx) :
    process_pool     = None;
    restart_all_flag = False;
    server_ctx['logger'].info( "Marian NMT monitor sub thread is running pid.<{}>".format( os.getpid()) );

    while True :
        restart_all_flag = False;

        #-- 监控所有的子进程 --#
        if process_pool is not None :
            for sub_proc in process_pool :
                if sub_proc is not None :
                    if False == sub_proc.is_alive() :
                        #-- 其中一个挂了都进行重启 --#
                        restart_all_flag = True;
                        break;
                else :
                    restart_all_flag = True;
                    break;
        else :
            restart_all_flag = True;

        #-- 需要重启吗??? --#
        if restart_all_flag :
            if process_pool is not None :
                for sub_proc in process_pool:
                    if sub_proc is not None :
                        #-- 终止 --#
                        sub_proc.terminate();
                        sub_proc.join();

            #-- 重新创建队列 --#
            server_ctx['worker_ctx']['lock'].acquire();

            server_ctx['worker_ctx']['queue' ] = [];
            server_ctx['worker_ctx']['rqueue'] = [];
            server_ctx['worker_ctx']['queue']  = [None] * server_ctx['n_process'];
            server_ctx['worker_ctx']['rqueue'] = [None] * server_ctx['n_process'];
            server_ctx['worker_ctx']['req_lock' ]  = [None] * server_ctx['n_process'];
            server_ctx['worker_ctx']['resp_lock' ] = [None] * server_ctx['n_process'];

            for i in xrange( int( server_ctx['n_process'])) :
                server_ctx['worker_ctx']['queue' ][ i] = Queue( 1024);
                server_ctx['worker_ctx']['rqueue'][ i] = Queue( 1024);
                server_ctx['worker_ctx']['req_lock' ][ i] = Lock();
                server_ctx['worker_ctx']['resp_lock'][ i] = Lock();

            #-- 解锁 --#
            server_ctx['worker_ctx']['lock'].release();

            #-- 启动 --#
            process_pool = None;
            process_pool = nmt_load_model.instance( server_ctx['worker_ctx'],
                                                    server_ctx['models'], 
                                                    server_ctx['source_file'], 
                                                    server_ctx['saveto'], 
                                                    save_alignment= True, 
                                                    k             = server_ctx['k'],
                                                    normalize     = False, 
                                                    n_process     = server_ctx['n_process'], 
                                                    chr_level     = False, 
                                                    verbose       = False, 
                                                    nbest         = False, 
                                                    suppress_unk  = server_ctx['suppress_unk'], 
                                                    a_json        = False, 
                                                    print_word_probabilities= False, 
                                                    return_hyp_graph        = False, 
                                                    logger                  = server_ctx['logger'], 
                                                    pidfile                 = server_ctx['pidfile'],
                                                    devices_list = server_ctx['devices_list']
                                                  );
            

            #-- 记录所有子进程日志 --#
            for sub_proc in process_pool :
                if sub_proc is not None :
                    server_ctx['logger'].info( 'Parent.pid.<{}> start load_model subprocess.pid.<{}> is alive.<{}>'.format( os.getpid(), sub_proc.pid, sub_proc.is_alive()) );

        #-- 一秒检测一次 --#
        time.sleep( 1);
    pass;
#-- end->Func: Server: monitor_instance --#
    
