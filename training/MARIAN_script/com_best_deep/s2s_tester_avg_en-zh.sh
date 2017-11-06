#!/bin/bash

# model prefix
prefix=LSTM_ATTEN_model_en-zh_world/model_revo_s2s.avg.npz

dev=/home/revo/workshop/competition/cheat/world/test.bpe.en
ref=/home/revo/workshop/competition/cheat/world/true.bpe.zh

# decode

cat $dev | /home/revo/marian/build/s2s -c $prefix.yml -m $prefix -b 20 -n --mini-batch 1 --maxi-batch 1 2>/dev/null \
> $dev.output.postprocessed

# get BLEU
/home/revo/marian/examples/training/moses-scripts/scripts/generic/multi-bleu.perl $ref < $dev.output.postprocessed | cut -f 3 -d ' ' | cut -f 1 -d ','
