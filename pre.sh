#!/bin/bash

if [ "$1" == "-h"  ]; then

  echo 'Usage : ./preprocess.sh en zh corpus script_folder'
    exit 0
fi

# source language (example: fr)
S=en
# target language (example: en)
T=zh
# data
P=Bi-Health-en-zh-filter
# data folder
#PATH=$4
# script folder
P1=.


# learn BPE on joint vocabulary:
echo "Learning BPE"
cat ${P}.${S} ${P}.${T} | python $P1/learn_bpe.py -s 120000 > ${S}${T}.bpe
echo "Applying BPE"
python $P1/apply_bpe.py -c ${S}${T}.bpe < ${P}.${S} > ${P}.bpe.${S}
python $P1/apply_bpe.py -c ${S}${T}.bpe < ${P}.${T} > ${P}.bpe.${T}

NUM=40000
CORPUS=${P}.bpe
TERM=Health
SRCL=en
TGTL=zh
paste -d $'\t' $CORPUS.$SRCL $CORPUS.$TGTL | shuf > $CORPUS.shuf
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f1 > valid.$TERM.$SRCL-$TGTL.$SRCL
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f2 > valid.$TERM.$SRCL-$TGTL.$TGTL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f1 > train.$TERM.$SRCL-$TGTL.$SRCL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f2 > train.$TERM.$SRCL-$TGTL.$TGTL

