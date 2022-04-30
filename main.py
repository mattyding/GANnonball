import numpy as np
import preprocessing
import matplotlib.pyplot as plt

data = preprocessing.loadData()

#Generate a list of 5000 int between 1200,5500
M = 5000

#Convert to 50 x 100 list
n = len(data[0])
newList = [data[i:i+n] for i in range(0, len(data), n)]

#Convert to 50 x 100 numpy array
# print nArray
print(data.shape)
data = data.T

plt.imshow(data, cmap='hot', aspect='auto')
plt.colorbar()
plt.show()
