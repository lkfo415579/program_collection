#!/bin/bash

# model prefix

dev=~/workshop/competition/test.bpe.en

# decode

cat $dev | ~/marian/build/amun -c com_model-en-zh/model_revo_amun.avg.amun.yml -b 20 -n --mini-batch 10 --maxi-batch 130 -u 2>/dev/null \
> $dev.output.postprocessed

# get BLEU
#/home/revo/marian/examples/training/moses-scripts/scripts/generic/multi-bleu.perl $ref < $dev.output.postprocessed | cut -f 3 -d ' ' | cut -f 1 -d ','
