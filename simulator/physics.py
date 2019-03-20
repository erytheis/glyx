import numpy as np
from scipy.linalg import block_diag
import math

# Rotate the matrix using Euler angles
# credit to https://stackoverflow.com/questions/50295457/euler-rotation-of-ellipsoid-expressed-by-coordinate-matrices-in-python


DEFAULT_ORIENTATION = (0, 0, 1)


def rotate_vector(v, xyz):
    TD = np.multiply.outer(np.exp(1j * np.asanyarray(xyz)), [[1], [1j]]).view(float)
    x, y, z = (block_diag(1, TD[i])[np.ix_(*2 * (np.arange(-i, 3 - i),))] for i in range(3))
    return v @ (x @ y @ z)


def get_orientation_from_vectors(u, v):
    x_angle = math.acos(np.dot([u[1], u[2]], [v[1], v[2]]))
    y_angle = math.acos(np.dot([u[0], u[2]], [v[0], v[2]]))
    z_angle = math.acos(np.dot([u[0], u[1]], [v[0], v[1]]))
    return (x_angle, y_angle, z_angle)
