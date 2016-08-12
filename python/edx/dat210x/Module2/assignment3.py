import pandas as pd

# TODO: Load up the dataset
# Ensuring you set the appropriate header column names
#
# .. your code here ..
df = pd.read_csv('Datasets/servo.data', names=['motor', 'screw', 'pgain', 'vgain', 'class'], skipinitialspace=True)

# TODO: Create a slice that contains all entries
# having a vgain equal to 5. Then print the 
# length of (# of samples in) that slice:
#
# .. your code here ..
vgain5 = df[df['vgain']==5]
print("vgain: " + str(len(vgain5)))

# TODO: Create a slice that contains all entries
# having a motor equal to E and screw equal
# to E. Then print the length of (# of
# samples in) that slice:
#
# .. your code here ..
# motoree = df.loc[:,['motor','screw']]
motoree = df.loc[(df['motor'] == 'E') & (df['screw'] == 'E')]
print("motoree: " + str(len(motoree)))

# TODO: Create a slice that contains all entries
# having a pgain equal to 4. Use one of the
# various methods of finding the mean vgain
# value for the samples in that slice. Once
# you've found it, print it:
#
# .. your code here ..
pgain4 = df.loc[df['pgain'] == 4]
print(pgain4['vgain'].mean())


# TODO: (Bonus) See what happens when you run
# the .dtypes method on your dataframe!



