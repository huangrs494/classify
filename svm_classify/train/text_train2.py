# coding:utf-8
# 时间2017年6月16日16:06:55时确定可行的版本。。
import os
import codecs
import cPickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC, SVC
import jieba
import cPickle as pickle
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


def get_num(train_file, model_road=u"../april_model"):
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

    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.9, stop_words='english')#最大频率大于0.9的停用词删除。对数词频调整，sublinear_tf设置为true。文档转换成特征矩阵
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


# train_file1 = u"../../初步抽取的数据/april_data2_1.txt"
train_file1 = u"../../初步抽取的数据/april_data2_1_balance1.txt"
model_road1 = u"../april_model"
all_data, all_cate = get_num(train_file1, model_road1)  # 获取数值化的标签和数据；

train_data, test_data, train_cate, test_cate = train_test_split(all_data, all_cate, test_size=0.2)
#c惩罚因子默认是1.0
clf = LinearSVC(penalty="l2", loss='squared_hinge', dual=True, tol=1e-4,
                C=0.30, multi_class='ovr', fit_intercept=True,
                intercept_scaling=1, class_weight=None, verbose=0,
                random_state=None, max_iter=1000)  # 使用最佳参数进行训练模型。
clf.fit(train_data, train_cate)

with open("../april_model/linear_svc.pkl", "wb") as model_fw:  # 将分类模型载入硬盘
    pickle.dump(clf, model_fw)
with open("../april_model/linear_svc.pkl", "rb") as model_fr:  # 将分类模型重新载入内存。
    clf2 = pickle.load(model_fr)

result = clf2.predict(test_data)

print accuracy_score(test_cate, result)  # 对自身的预测。
print confusion_matrix(test_cate, result)  # 混淆矩阵
