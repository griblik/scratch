# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 15:54:49 2016

@author: ntelford
"""

from sklearn.datasets import load_iris
from pandas.tools.plotting import parallel_coordinates

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.style.use('ggplot')

data = load_iris()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target_names'] = [data.target_names[i] for i in data.target]

plt.figure()
parallel_coordinates(df, 'target_names')
plt.show()