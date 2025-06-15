import numpy as np

c = np.convolve(((1,2,3), (4,5,6), (7,8,9)), ((0,1), (0.5, 0)))

print (c)


