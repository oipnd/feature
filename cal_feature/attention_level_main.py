import numpy as np
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from cal_feature.MousefeaGet import HumanSectionData
import warnings

def prepro(raw_feature, raw_labels):
    #features = preprocessing.normalize(raw_feature, norm='l2')
    imp=preprocessing.Imputer(missing_values='NaN',
                              strategy='median',axis=0,
                              verbose=0,copy='true')
    #pre_feature=imp.fit(raw_feature)
    features = preprocessing.scale(imp.fit(raw_feature).transform(raw_feature))
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


def classify(features, labels):
    X_train, X_test, y_train, y_test = \
        train_test_split(features, labels, random_state=0)

    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)

    y_pred = knn.predict(X_test)
    c = confusion_matrix(y_test, y_pred)
    print(np.mean(y_pred == y_test))
    print(knn.score(X_test, y_test))
    print(c)


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    path='D:\data\pc'
    raw_fea,raw_label=HumanSectionData(path)
    fea,label=prepro(raw_fea,raw_label)
    print(fea.dtype)
    print(label)

