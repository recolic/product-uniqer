from uniqer import *

import numpy as np

m = np.matrix([
    [1,2,3],
    [6,2,8],
    [876,3,35],
    [12,5,23],
    [-1,55,2],
    [1,1,1],
    [1,2,3],
    [9,1,1]
],dtype=str)
print(m)
print(uniq(m,(0,1),2))