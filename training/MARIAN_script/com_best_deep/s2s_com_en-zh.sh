#!/bin/bash

# model prefix
#prefix=com_model-en-zh_2/model_revo_s2s.npz.best-cross-entropy.npz
prefix=LSTM_ATTEN_model_en-zh/model_revo_s2s.npz.best-cross-entropy.npz

dev=/home/revo/workshop/competition/cheat/test.bpe.en
ref=/home/revo/workshop/competition/cheat/true.tok.zh

# decode

cat $dev | /home/revo/marian/build/s2s -c $prefix.yml -m $prefix -b 20 -n --mini-batch 1 --maxi-batch 1 2>/dev/null \
| sed 's/\@\@ //g' | ~/moses-scripts/scripts/recaser/detruecase.perl > $dev.output.postprocessed

# get BLEU
/home/revo/marian/examples/training/moses-scripts/scripts/generic/multi-bleu.perl $ref < $dev.output.postprocessed | cut -f 3 -d ' ' | cut -f 1 -d ','
