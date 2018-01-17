# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys
from regex import Regex
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    if sys.argv[1] == '-h':
        print "Usage python sum_two_corpus.py [source_prefix] [target_prefix] [posfix]"
        sys.exit()
    s_prefix = sys.argv[1]
    t_prefix = sys.argv[2]
    pos_fix = sys.argv[3]
    output_file_s = codecs.open("tmp_output.1", "wa")
    output_file_t = codecs.open("tmp_output.2", "wa")

    for i in xrange(30):
        tmp_s_file_path = s_prefix+str(i)+pos_fix
        tmp_t_file_path = t_prefix+str(i)+pos_fix
        try:
            source_file = codecs.open(tmp_s_file_path, "rb").readlines()
            target_file = codecs.open(tmp_t_file_path, "rb").readlines()
        except IOError:
            continue
        #
        for num, s_line in enumerate(source_file):
            t_line = target_file[num]
            if s_line.strip() == "" or t_line.strip() == "":
                continue
            output_file_s.write(s_line.strip()+'\n')
            output_file_t.write(t_line.strip()+'\n')
