import pandas as pd
import numpy as np


# TODO:
# Load up the dataset, setting correct header labels
# Use basic pandas commands to look through the dataset...
# get a feel for it before proceeding!
# Find out what value the dataset creators used to
# represent "nan" and ensure it's properly encoded as np.nan
#
# .. your code here ..
df = pd.read_csv('Datasets/census.data', sep=",", names=['uid','education', 'age', 'capital-gain', 'race', 'capital-loss', 'hours-per-week', 'sex', 'classification'], na_values=['0'])
df = df.drop('uid',axis=1)
# TODO:
# Figure out which features should be continuous + numeric
# Conert these to the appropriate data type as needed,
# that is, float64 or int64
#
# .. your code here ..



# TODO:
# Look through your data and identify any potential categorical
# features. Ensure you properly encode any ordinal types using
# the method discussed in the chapter.
#
# .. your code here 

ordered_classification = ['<=50K','>50K']
df.classification = df.classification.astype('category',ordered=True,categories=ordered_classification).cat.codes

# ord_ed = ['Preschool','1st-4th','5th-6th','7th-8th','9th','10th','11th','12th','HS-grad','Some-college','Bachelors','Masters','Doctorate']
# df.education = df.education.astype('category', ordered=True, categories=ord_ed).cat.codes

# TODO:
# Look through your data and identify any potential categorical
# features. Ensure you properly encode any nominal types by
# exploding them out to new, separate, boolean fatures.
#
# .. your code here ..

df = pd.get_dummies(df,columns=['race'])
df = pd.get_dummies(df,columns=['education'])

# TODO:
# Print out your dataframe
print(df)
df['age'].plot()