# coding:utf-8

import os
import sys
import codecs
from collections import defaultdict



new_file = u"C:/.../july_data.txt"
new_file2 = u"C:/...../july_data2.txt"
all_text = defaultdict(int)

with codecs.open(new_file, "r", "utf-8") as fr:
    for line in fr:
        line1 = line.strip().split("\t",1)

        if len(line1) != 2:
            continue
        all_text[line1[1]] += 1

with codecs.open(new_file, "r", "utf-8") as fr, codecs.open(new_file2, "w", "utf-8") as fw:
    for line in fr:
        line1 = line.strip().split("\t", 1)
        print type(all_text)
        print line1[1]
        if line1[1] in all_text:
            fw.write(u"{}".format(line))
            del all_text[line1[1]]




