# coding:utf-8
# 这个相当于是网格搜索来寻求最佳参数的代码
import os
import codecs
import cPickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC, SVC
import jieba
import cPickle as pickle
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split, KFold, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from numpy import cov, mean
import numpy as np


def get_num(train_file, model_road=u"../model"):
    cate1 = list()
    data = list()
    with codecs.open(train_file, "r", "utf-8") as fr:
        for line in fr:
            line1 = line.strip().split("\t", 2)
            cate1.append(line1[1])
            one_data = " ".join(jieba.cut(line1[2]))
            data.append(one_data)
    cate_set = list(set(cate1))  # 标签的集合
    cate = [cate_set.index(cat) for cat in cate1]  # 根据集合转换为数字标签

    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.9, stop_words='english')
    all_train_data = vectorizer.fit_transform(data)
    # for word, num in vectorizer.vocabulary_.iteritems():
    #     print word, num
    print len(vectorizer.vocabulary_.keys())
    vectorizer.cate_set = cate_set
    print " ".join(cate_set)

    if not os.path.exists(model_road):  # 如果不存在模型文件，则创建
        os.makedirs(model_road)
    tf_idf_file = os.path.join(model_road, "svmTFIDFModel.pkl")
    cPickle.dump(vectorizer, open(tf_idf_file, "wb"))  # 模型dump下来
    return all_train_data, cate


def main():
    # train_file1 = u"../../初步抽取的数据/april_data2_1.txt"
    train_file1 = u"../../初步抽取的数据/april_data2_1_balance1.txt"
    model_road1 = u"../model"
    all_data, all_cate = get_num(train_file1, model_road1)  # 获取数值化的标签和数据；

    C = np.arange(0.24, 0.36, 0.02)#0.36
    for one_c in C:  # 经过循环迭代后发现，0.28-0.34效果较好，故可选择0.30作为参数
        clf = LinearSVC(penalty="l2", loss='squared_hinge', dual=True, tol=1e-4,
                        C=one_c, multi_class='ovr', fit_intercept=True,
                        intercept_scaling=1, class_weight=None, verbose=0,
                        random_state=None, max_iter=1000)

        scores = cross_val_score(clf, all_data, all_cate, cv=10)  # 简单交叉验证（应该是K折交叉把，K=10）
        print "惩罚因子", one_c, "交叉验证的结果：均值和方差：", mean(scores), cov(scores)


if __name__ == '__main__':
    main()
