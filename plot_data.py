import numpy as np
import preprocessing
import matplotlib.pyplot as plt

data = preprocessing.loadData()

song1 = data[0]
print(len(data))

# n = len(song1[0])
song1 = song1.T

# for i in range(len(song1)):
#         for j in range(len(song1[i])):
#             # print(img[i][j])
#             song1[i][j] = 1 if song1[i][j] > 0 else 0

plt.imshow(song1, cmap='hot')
plt.show()
