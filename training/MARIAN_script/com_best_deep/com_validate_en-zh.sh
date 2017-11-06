#!/bin/bash

# model prefix
prefix=com_model-en-zh_2/model_revo_amun.npz

dev=~/workshop/competition/valid.tok.bpe.en
ref=~/workshop/competition/valid.tok.bpe.zh

# decode

cat $dev | ~/marian/build/amun -c $prefix.dev.npz.amun.yml -b 12 -n --mini-batch 10 --maxi-batch 100 2>/dev/null \
> $dev.output.postprocessed

# get BLEU
/home/revo/marian/examples/training/moses-scripts/scripts/generic/multi-bleu.perl $ref < $dev.output.postprocessed | cut -f 3 -d ' ' | cut -f 1 -d ','
