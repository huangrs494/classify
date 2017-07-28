#  -*- coding:utf-8 -*-

import os
import csv
import codecs

#通用模型，6，7月份预测分类的通用模型



may_new_file = u"C:/..../july_data.txt"
#五月份的数据转换成txt:
if os.path.exists(may_new_file):
    os.remove(may_new_file)
with codecs.open(may_new_file, "a", "utf-8") as fw:
        csv_reader = csv.reader(csv_file)
        try:  # _csv.Error: line contains NULL byte
            for row in csv_reader:
                if len(row) < 7:  # 这个是什么原因呢，为什么会有空行
                    continue

                if row[0].decode("gbk", "ignore") == u"37e4364c20914f8a898d29ad23448245":
                    continue
                #label = row[7].decode("gbk", "ignore").strip().replace("\n", " ")
                data = row[6].decode("gbk", "ignore").strip().replace("\n", " ")
                if row[3].decode("gbk", "ignore") == u"访客"  and len(data) > 0:
                    fw.write(u"{}\t{}\r\n".format(row[0].decode("gbk", "ignore").strip(),data))
        except csv.Error, e:
            print 'file %s: %s' % (may_new_file, e)
