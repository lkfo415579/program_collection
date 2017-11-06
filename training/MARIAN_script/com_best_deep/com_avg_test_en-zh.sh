#!/bin/bash

# model prefix

dev=~/workshop/competition/test.bpe.en

# decode

cat $dev | ~/marian/build/amun -c com_mix/model_revo_amun.avg.amun.yml -b 20 -n --mini-batch 10 --maxi-batch 100 2>/dev/null \
    | /home/revo/marian/examples/training/moses-scripts/scripts/recaser/detruecase.perl > $dev.output.postprocessed

# get BLEU
#/home/revo/marian/examples/training/moses-scripts/scripts/generic/multi-bleu.perl $ref < $dev.output.postprocessed | cut -f 3 -d ' ' | cut -f 1 -d ','
