from uniqer import *

import numpy as np

m = np.matrix([
    [1,2,3,1],
    [6,2,8,2],
    [876,3,35,1],
    [12,5,23,0],
    [-1,55,2,0],
    [1,1,1,0],
    [1,2,44,2],
    [9,1,1,0]
],dtype=str)
print(m)
print(uniq(m,(0,1),(2,3)))