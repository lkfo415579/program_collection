NUM=30000
CORPUS=Bi-News-en-zh-clean.bpe
TERM=News
SRCL=en
TGTL=zh
paste -d $'\t' $CORPUS.$SRCL $CORPUS.$TGTL | shuf > $CORPUS.shuf
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f1 > valid.$TERM.$SRCL-$TGTL.$SRCL
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f2 > valid.$TERM.$SRCL-$TGTL.$TGTL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f1 > train.$TERM.$SRCL-$TGTL.$SRCL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f2 > train.$TERM.$SRCL-$TGTL.$TGTL

NUM=30000
CORPUS=Bi-News-zh-en-clean.bpe
TERM=News
SRCL=zh
TGTL=en
paste -d $'\t' $CORPUS.$SRCL $CORPUS.$TGTL | shuf > $CORPUS.shuf
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f1 > valid.$TERM.$SRCL-$TGTL.$SRCL
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f2 > valid.$TERM.$SRCL-$TGTL.$TGTL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f1 > train.$TERM.$SRCL-$TGTL.$SRCL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f2 > train.$TERM.$SRCL-$TGTL.$TGTL


NUM=40000
CORPUS=Bi-Training-ja-zh-clean.bpe
TERM=JP
SRCL=ja
TGTL=zh
paste -d $'\t' $CORPUS.$SRCL $CORPUS.$TGTL | shuf > $CORPUS.shuf
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f1 > valid.$TERM.$SRCL-$TGTL.$SRCL
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f2 > valid.$TERM.$SRCL-$TGTL.$TGTL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f1 > train.$TERM.$SRCL-$TGTL.$SRCL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f2 > train.$TERM.$SRCL-$TGTL.$TGTL


NUM=40000
CORPUS=Bi-Training-en-pt-clean.bpe
TERM=General
SRCL=en
TGTL=pt
paste -d $'\t' $CORPUS.$SRCL $CORPUS.$TGTL | shuf > $CORPUS.shuf
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f1 > valid.$TERM.$SRCL-$TGTL.$SRCL
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f2 > valid.$TERM.$SRCL-$TGTL.$TGTL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f1 > train.$TERM.$SRCL-$TGTL.$SRCL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f2 > train.$TERM.$SRCL-$TGTL.$TGTL

NUM=40000
CORPUS=Bi-Training-de-en-clean.bpe
TERM=General
SRCL=de
TGTL=en
paste -d $'\t' $CORPUS.$SRCL $CORPUS.$TGTL | shuf > $CORPUS.shuf
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f1 > valid.$TERM.$SRCL-$TGTL.$SRCL
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f2 > valid.$TERM.$SRCL-$TGTL.$TGTL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f1 > train.$TERM.$SRCL-$TGTL.$SRCL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f2 > train.$TERM.$SRCL-$TGTL.$TGTL


NUM=30000
CORPUS=train.tok.clean.NUM.bpe
TERM=COM
SRCL=en
TGTL=zh
paste -d $'\t' $CORPUS.$SRCL $CORPUS.$TGTL | shuf > $CORPUS.shuf
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f1 > valid.$TERM.$SRCL-$TGTL.$SRCL
head -n $NUM $CORPUS.shuf | cut -d $'\t' -f2 > valid.$TERM.$SRCL-$TGTL.$TGTL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f1 > train.$TERM.$SRCL-$TGTL.$SRCL
sed '1,'$NUM'd' $CORPUS.shuf | cut -d $'\t' -f2 > train.$TERM.$SRCL-$TGTL.$TGTL

