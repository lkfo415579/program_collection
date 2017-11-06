#!/bin/bash

# set chosen gpus
GPUS="0 1 2"
SRCL=en
TGTL=zh
CORPUS=train.tok.bpe
CORPUS_DIR=/home/revo/workshop/competition
MODELS_DIR=com_model-en-zh_2
DEV_SET=valid.tok.bpe
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
        --devices $GPUS --seed 6 \
        --train-sets $CORPUS_DIR/$CORPUS.$SRCL $CORPUS_DIR/$CORPUS.$TGTL \
        --max-length 120 \
        --vocabs $MODELS_DIR/vocab.$SRCL.yml $MODELS_DIR/vocab.$TGTL.yml \
        --dim-vocabs 68888 66666 \
        --dynamic-batching -w 4000\
        --best-deep \
        --layer-normalization --dropout-rnn 0.2 --dropout-src 0.1 --dropout-trg 0.1 \
        --early-stopping 5 --moving-average \
        --dim-emb 512 \
        --tied-embeddings \
        --valid-freq 25000 --save-freq 50000 --disp-freq 1000 \
        --valid-sets $CORPUS_DIR/$DEV_SET.$SRCL $CORPUS_DIR/$DEV_SET.$TGTL \
        --valid-metrics cross-entropy \
        --keep-best \
        --embedding-normalization \
        --embedding-fix-src \
        --embedding-fix-trg \
        --log $MODELS_DIR/train.log --valid-log $MODELS_DIR/valid.log


#--tied-embeddings
