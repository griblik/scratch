import pandas as pd

# TODO: Load up the 'tutorial.csv' dataset
#
# .. your code here ..
df = pd.read_csv('Datasets/tutorial.csv')


# TODO: Print the results of the .describe() method
#
# .. your code here ..
print(df)
print('\n')
print(df.describe())
print('\n')

# TODO: Figure out which indexing method you need to
# use in order to index your dataframe with: [2:4,'col3']
# And print the results
#
# .. your code here ..

print(df.loc[2:3,'col3'])