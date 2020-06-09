import warnings

import numpy as np
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
# from sklearn.gaussian_process import GaussianProcess
from sklearn.tree import DecisionTreeClassifier

from cal_feature.MousefeaGet import HumanSectionData

# raw_feature = np.load('D:\\data\\fea_lab\\feature.npy', mmap_mode=None, allow_pickle=True, fix_imports=True,
#                       encoding='ASCII')
# raw_labels = np.load('D:\\data\\fea_lab\\label.npy', mmap_mode=None, allow_pickle=True, fix_imports=True,
#                      encoding='ASCII')


def prepro(raw_feature, raw_labels):
    # features = preprocessing.normalize(raw_feature, norm='l2')
    # imp=sklearn.preprocessing.Imputer(missing_values='NaN',
    #                           strategy='median',axis=0,
    #                           verbose=0,copy='true')
    # #pre_feature=imp.fit(raw_feature)
    # features = preprocessing.scale(imp.fit(raw_feature).transform(raw_feature))

    features = raw_feature

    where_are_nan = np.isnan(raw_feature)
    where_are_inf = np.isinf(raw_feature)
    raw_feature[where_are_nan] = 0
    raw_feature[where_are_inf] = 0

    labels = []
    it = iter(raw_labels)
    for label in it:
        if label < 3000:
            labels.append('high')
        elif 6000 > label >= 3000:
            labels.append('medium')
        else:
            labels.append('low')

    return features, labels


h = .02  # step size in the mesh


def classify(features, labels):
    X_train, X_test, y_train, y_test = \
        train_test_split(features, labels, random_state=0)
    names = ["Nearest Neighbors", "RBF SVM",
             "Decision Tree", "Random Forest", "AdaBoost",
             "Naive Bayes", "QDA", "Gaussian Process", "Neural Net", ]

    classifiers = [
        KNeighborsClassifier(3),
        # SVC(kernel="linear", C=0.025),
        SVC(gamma=2, C=1),
        DecisionTreeClassifier(max_depth=5),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        AdaBoostClassifier(),
        GaussianNB(),
        QuadraticDiscriminantAnalysis(),
    ]
    i = 1
    for name, clf in zip(names, classifiers):
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)
        y_pred = clf.predict(X_test)
        c = confusion_matrix(y_test, y_pred)
        print(name)
        print(np.mean(y_pred == y_test))
        print(score)
        print(c)
        print(i)
        i = i + 1
    # knn = KNeighborsClassifier(n_neighbors=1)
    # knn.fit(X_train, y_train)
    #
    # y_pred = knn.predict(X_test)
    # c = confusion_matrix(y_test, y_pred)
    # print(np.mean(y_pred == y_test))
    # print(knn.score(X_test, y_test))
    # print(c)


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    path = 'D:\data\pc'
    raw_fea, raw_label = HumanSectionData(path)
    fea, label = prepro(raw_fea, raw_label)
    classify(fea, label)
    print('finish')
