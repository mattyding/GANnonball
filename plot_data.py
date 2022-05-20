import numpy as np
import preprocessing
import matplotlib.pyplot as plt

data = preprocessing.loadData()

song1 = data[0]
print(len(data))

# n = len(song1[0])
song1 = song1.T

plt.imshow(song1, cmap='hot', aspect='auto')
plt.colorbar()
plt.show()
