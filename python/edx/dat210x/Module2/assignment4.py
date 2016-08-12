import pandas as pd


# TODO: Load up the table, and extract the dataset
# out of it. If you're having issues with this, look
# carefully at the sample code provided in the reading
#
# .. your code here ..
dfall = pd.read_html(io='http://espn.go.com/nhl/statistics/player/_/stat/points/sort/points/year/2015/seasontype/2', skiprows=0)

# TODO: Rename the columns so that they match the
# column definitions provided to you on the website
#
# .. your code here ..
df = dfall[0]
df.columns = ['RK','Player','Team','GP','G','A','PTS','+/-','PIM','PTS/G','SOG','PCT','GWG','PPG','PPA','SHG','SHA']

# TODO: Get rid of any row that has at least 4 NANs in it
#
# .. your code here ..
df = df.dropna(axis=0, thresh=4)


# TODO: At this point, look through your dataset by printing
# it. There probably still are some erroneous rows in there.
# What indexing command(s) can you use to select all rows
# EXCEPT those rows?
#
# .. your code here ..
df = df.loc[df['RK'] != 'RK']

# TODO: Get rid of the 'RK' column
#
# .. your code here ..
df = df.drop(labels="RK",axis=1)

# TODO: Ensure there are no holes in your index by resetting
# it. By the way, don't store the original index
#
# .. your code here ..
df = df.reset_index()


# TODO: Check the data type of all columns, and ensure those
# that should be numeric are numeric
df.GP = pd.to_numeric(df.GP)
df.G = pd.to_numeric(df.G)
df.A = pd.to_numeric(df.A)
df.PTS = pd.to_numeric(df.PTS)
df['+/-'] = pd.to_numeric(df['+/-'])
df.PIM = pd.to_numeric(df.PIM)
df['PTS/G'] = pd.to_numeric(df['PTS/G'])
df.SOG = pd.to_numeric(df.SOG)
df.PCT = pd.to_numeric(df.PCT)
df.GWG = pd.to_numeric(df.GWG)
df.PPA = pd.to_numeric(df.PPA)
df.PPG = pd.to_numeric(df.PPG)
df.SHG = pd.to_numeric(df.SHG)
df.SHA = pd.to_numeric(df.SHA)

# TODO: Your dataframe is now ready! Use the appropriate 
# commands to answer the questions on the course lab page.



print("df:\n")
print(df.describe())
print(len(df.PCT.unique()))
print(df.GP[15] + df.GP[16])

