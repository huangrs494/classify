#!/usr/bin/env python
#encoding: utf-8
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
# import re

#分类标签的关键词字典

#给每一个关键词打上标签,比如第一行的的是{艾：艾灸}
f = open(u"E:/pycharm_project/important_msg/抽取的数据/findwd.txt")
t = f.readlines()
line_topic_map = {2: u'艾灸', 3: u"生活", 4: u'娱乐'}
key_line_map = {} # 关键字对应的行数的MAP, 比如 {"艾": [0,2]}
for inx, i in enumerate(t):
    if inx == 0:
        continue
    keys = i.strip('\n').strip('\r').split('\t')
    for key in keys:
        if not key_line_map.get(key):
            key_line_map[key] = [line_topic_map[inx + 1]]
        else:
            key_line_map[key] = key_line_map[key].append(line_topic_map[inx + 1])
f.close()


#如果findwd里面的词语出现再话题内容中，则给话题内容打上findwd中词的标签
f = open(u'E:/pycharm_project/important_msg/抽取的数据/tt_Topic.txt')
t = f.readlines()
fw = open(u'E:/pycharm_project/important_msg/抽取的数据/liujun_Topic.txt','w')
for inx, i in enumerate(t):
    tt_line_list = i.strip("\n").split('\t')
    topic_name = tt_line_list[2]
    topic_intr = tt_line_list[3]

    #topic_name, topic_intr
    topids = []

    for k, v in key_line_map.items():
        if k in topic_name or k in topic_intr:
            topids.extend(v)
    topids = list(set(topids))
    if inx != 0:
        if topids == []:
            topids = ['其他']

    print inx, topic_name, topic_intr, (' ').join(topids)
    fw.write(u"{}\t{}\t{}\t{}\r\n".format(inx, topic_name, topic_intr, (' ').join(topids)))