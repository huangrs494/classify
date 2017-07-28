# coding:utf-8

import os
import codecs
import cPickle
import jieba
import cPickle as pickle


def get_num(test_file, vectorizer):
    data = list()
    with codecs.open(test_file, "r", "utf-8") as fr:
        for line in fr:
            line1 = line.strip().split("\t", 1)
            one_data = " ".join(jieba.cut(line1[1]))
            data.append(one_data)

    all_test_data = vectorizer.transform(data)
    return all_test_data

# 这四五行是下载tfidf的转化模型 #
model_road=u"../april_model"
tf_idf_file = os.path.join(model_road, "svmTFIDFModel.pkl")
with open(tf_idf_file, "rb") as tfidf_fr:
    vectorizer1 = cPickle.load(tfidf_fr)  # 模型dump下来
cate_set = vectorizer1.cate_set

# 根据tfidf转化模型将测试数据转换为数值型 #
# test_file = u"../../初步抽取的数据/april_data2_1_test.txt"
# predict_file = u"../../初步抽取的数据/april_data2_1_predict.txt"

test_file = u"C:\.....20170721待分类.txt"
predict_file = u"C:\......20170721已分类.txt"
all_test_data = get_num(test_file, vectorizer1)


with open("../april_model/linear_svc.pkl", "rb") as model_fr:  # 将分类模型重新载入内存。
    clf2 = pickle.load(model_fr)

result = clf2.predict(all_test_data)
label = [cate_set[i] for i in result]
with codecs.open(test_file, "r", "utf-8") as fr, codecs.open(predict_file, "w", "utf-8") as fw:
    for line,one_label in zip(fr,label):
        line1 = line.strip().split("\t", 1)
        fw.write(u"{}\t{}\t{}\r\n".format(line1[0],one_label,line1[1]))










