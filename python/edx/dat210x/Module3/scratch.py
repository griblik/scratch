# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 12:18:03 2016

@author: ntelford
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# read data and drop the NaNs
df = pd.read_csv('Datasets/wheat.data')
df = df.dropna(axis=0)

# wheat_type is canadian, koma or something else. Map to a category.
df['wheat_type'] = df['wheat_type'].astype("category").cat.codes


pca = PCA(n_components=3)
pca.fit(df)

T = pca.transform(df)

print(df.shape)
print('=======')
print(T.shape)

plt.scatter(T[2],T[3])