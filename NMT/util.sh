cat valid.log | grep cross | sort -g -k8,8 -t ' ' | cut -f 4 -d ' ' | head -n 4 | xargs -I {} echo model_revo_s2s.iter{}.npz
scp  revo@10.0.100.182:/home/revo/workshop/com_best_deep/tester

#fast align
perl prepare-fast-align.perl ~/workshop/competition/world/train.clean.en ~/workshop/competition/world/train.clean.zh > train.en-zh
./fast_align -i train.en-zh -d -o -v > forward.align
./fast_align -i train.en-zh -d -o -v -r > reverse.align
./old_atools -i forward.align -j reverse.align -c grow-diag-final-and > grow-diag-final-and
