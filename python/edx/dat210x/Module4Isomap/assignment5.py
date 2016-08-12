import pandas as pd

from scipy import misc
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np

# Look pretty...
matplotlib.style.use('ggplot')


#
# TODO: Start by creating a regular old, plain, "vanilla"
# python list. You can call it 'samples'.
#
# .. your code here .. 

samples = []

#
# TODO: Write a for-loop that iterates over the images in the
# Module4/Datasets/ALOI/32/ folder, appending each of them to
# your list. Each .PNG image should first be loaded into a
# temporary NDArray, just as shown in the Feature
# Representation reading.
#
# Optional: Resample the image down by a factor of two if you
# have a slower computer. You can also convert the image from
# 0-255  to  0.0-1.0  if you'd like, but that will have no
# effect on the algorithm's results.
#
# .. your code here .. 

locs = ['./Datasets/ALOI/32/', './Datasets/ALOI/32i/']
samples = []

for here in locs:
    imgs = [np.array(misc.imread(here + img)) for img in os.listdir(here)]
    
    for img in os.listdir(here):
        imgdata = misc.imread(here + img)
        sampledata = [item for sublist in imgdata for item in sublist]
        samples.append(sampledata)


df = pd.DataFrame(data=samples)

from sklearn.manifold import Isomap

im = Isomap(n_neighbors=6, n_components=3)
im.fit(df)

T = im.transform(df)

# 2d scatter
plt.scatter(T[:,0],T[:,1])


# 3d scatter
fig = plt.figure()
ax = fig.add_subplot(111,projection="3d")
ax.set_xlabel('0')
ax.set_ylabel('1')
ax.set_zlabel('2')

ax.scatter(T[:,0],T[:,1],T[:,2],marker='.')


plt.show()


#
# TODO: Once you're done answering the first three questions,
# right before you converted your list to a dataframe, add in
# additional code which also appends to your list the images
# in the Module4/Datasets/ALOI/32_i directory. Re-run your
# assignment and answer the final question below.
#
# .. your code here .. 


#
# TODO: Convert the list to a dataframe
#
# .. your code here .. 



#
# TODO: Implement Isomap here. Reduce the dataframe df down
# to three components, using K=6 for your neighborhood size
#
# .. your code here .. 



#
# TODO: Create a 2D Scatter plot to graph your manifold. You
# can use either 'o' or '.' as your marker. Graph the first two
# isomap components
#
# .. your code here .. 




#
# TODO: Create a 3D Scatter plot to graph your manifold. You
# can use either 'o' or '.' as your marker:
#
# .. your code here .. 



plt.show()

