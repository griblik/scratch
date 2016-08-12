import pandas as pd
import matplotlib.pyplot as plt


#
# TODO: Load up the Seeds Dataset into a Dataframe
# It's located at 'Datasets/wheat.data'
# 
# .. your code here ..
df = pd.read_csv('Datasets/wheat.data')

#
# TODO: Drop the 'id' feature
# 
# .. your code here ..

df = df.drop(['id'], axis=1)

#
# TODO: Compute the correlation matrix of your dataframe
# 
# .. your code here ..


#
# TODO: Graph the correlation matrix using imshow or matshow
# 
# .. your code here ..
print(df.corr())
plt.imshow(df.corr(), interpolation='nearest')
plt.colorbar()
tick_marks = [i for i in range(len(df.columns))]
plt.xticks(tick_marks, df.columns, rotation='vertical')
plt.yticks(tick_marks, df.columns)

plt.show()

