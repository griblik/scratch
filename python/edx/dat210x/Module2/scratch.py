# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

matplotlib.style.use('ggplot')
sd = pd.read_csv('./students.data', index_col=0)

my_series = sd['G3']
df = sd[['G3','G2','G1']]

fig = plt.figure()

ax = fig.add_subplot(111,projection='3d')
ax.set_xlabel('Final grade')
ax.set_ylabel('First grade')
ax.set_zlabel('Daily alcohol')

ax.scatter(sd['G1'], sd['G2'],sd['G3'], c='r', marker='.')

plt.show()

# my_series.plot.hist(alpha=0.5)
# df.plot.hist(alpha=0.5, normed=True, bins=20)

# df.plot.scatter('G1','G3')