import numpy as np
import preprocessing
import matplotlib.pyplot as plt

data = preprocessing.loadData()

n = len(data[0])
data = data.T

plt.imshow(data, cmap='hot', aspect='auto')
plt.colorbar()
plt.show()
