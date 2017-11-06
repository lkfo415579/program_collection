#!/bin/bash

# set chosen gpus
GPUS="0 1 2"
SRCL=en
TGTL=zh
CORPUS=train.clean
CORPUS_DIR=/home/revo/workshop/competition/world
MODELS_DIR=LSTM_ATTEN_model_en-zh_world
DEV_SET=valid.en-zh.bpe
if [ $# -ne 0 ]
then
    GPUS=$@
fi
echo Using gpus $GPUS


if [ ! -e $MODELS_DIR ]
then
    mkdir -p $MODELS_DIR
fi

# train model

    /home/revo/marian/build/marian \
        --model $MODELS_DIR/model_revo_s2s.npz \
        --type s2s \
        --devices $GPUS --seed 123 \
        --train-sets $CORPUS_DIR/$CORPUS.$SRCL $CORPUS_DIR/$CORPUS.$TGTL \
        --max-length 130 \
        --vocabs $MODELS_DIR/vocab.$SRCL.yml $MODELS_DIR/vocab.$TGTL.yml \
        --dim-vocabs 73333 76666 \
        --dynamic-batching -w 5000\
        --best-deep \
        --layer-normalization --dropout-rnn 0.2 --dropout-src 0.1 --dropout-trg 0.1 \
        --early-stopping 10 --moving-average \
        --dim-emb 555 \
        --tied-embeddings \
        --valid-freq 25000 --save-freq 50000 --disp-freq 1000 \
        --valid-sets $CORPUS_DIR/$DEV_SET.$SRCL $CORPUS_DIR/$DEV_SET.$TGTL \
        --valid-metrics cross-entropy \
        --keep-best \
        --lr-decay 0.1 \
        --dim-rnn 1024 \
        --enc-cell lstm \
        --embedding-fix-src --embedding-fix-trg \
        --guided-alignment $CORPUS_DIR/grow-diag-final-and \
        --log $MODELS_DIR/train.log --valid-log $MODELS_DIR/valid.log

#--dec-cell lstm
#--valid-script-path ./S2S_validate_en-zh.sh \
#--tied-embeddings
