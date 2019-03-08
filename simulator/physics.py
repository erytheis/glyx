import numpy as np
from scipy.linalg import block_diag
import math


# Rotate the matrix using Euler angles
# credit to https://stackoverflow.com/questions/50295457/euler-rotation-of-ellipsoid-expressed-by-coordinate-matrices-in-python
def rotate_vector(v, xyz):
    TD = np.multiply.outer(np.exp(1j * np.asanyarray(xyz)), [[1], [1j]]).view(float)
    x, y, z = (block_diag(1, TD[i])[np.ix_(*2 * (np.arange(-i, 3 - i),))] for i in range(3))
    return v @ (x @ y @ z)


