# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import sklearn.preprocessing as pp
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.manifold import Isomap

def findMaxSVC():
    maxScore = {}
    maxScore['score'] = 0
    maxScore['C'] = 0
    maxScore['gamma'] = 0
    
    for C in np.arange(0.05, 2, 0.05):
        for gamma in np.arange(0.001, 0.1, 0.001):
            
            model = SVC(C=C, gamma=gamma, kernel='rbf')
            model.fit(X_train, y_train)
            score = model.score(X_test, y_test)
            
            if score > maxScore['score']:
                maxScore['score'] = score
                maxScore['C'] = C
                maxScore['gamma'] = gamma
                
    return maxScore

# TODO: Load data into X and drop name
X = pd.read_csv('Datasets/parkinsons.data')
X = X.dropna()
#print(X.describe())
#print(X.dtypes)

X = X.drop('name', axis=1)

# TODO: splice status into y and drop it from X

y = X['status']
X = X.drop('status', axis=1)


# TODO: Scale X
#print('Unscaled\n========')

#X = pp.scale(X)
#print('Scaler\n========')

scaler = pp.StandardScaler().fit(X)
X = scaler.transform(X)
print('StandardScaler\n========')

#minmaxscaler = pp.MinMaxScaler()
#minmaxscaler.fit(X)
#X = minmaxscaler.transform(X)
#print('MinMaxScaler\n========')

#maxabsscaler = pp.MaxAbsScaler()
#maxabsscaler.fit(X)
#X = maxabsscaler.transform(X)
#print('MaxAbsScaler\n========')

#X = pp.normalize(X)
#print('normalizer\n========')

# TODO: Use PCA to reduce noise, n_components 4-14

nc = 5
#pca = PCA(n_components=nc)
#pca.fit(X)
#X = pca.transform(X)
#print('PCA: ', nc)

# Use Isomap to reduce noise, n_neighbors 2-5
nn = 4
im = Isomap(n_neighbors=nn, n_components=nc)
im.fit(X)
X = im.transform(X)
print('Isomap: ',nn, ' comp: ', nc)

# TODO: train_test_split 30% and random_state=7

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=7)

# TODO: Create an SVC, train and score against defaults
result = findMaxSVC()
print(result['score'])