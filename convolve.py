import numpy as np

c = np.convolve((1,2,3), (4,5,6))

print (c)

c1 = np.convolve((1,2,3, 4), (0, 1, 0.5))

print (c1)
