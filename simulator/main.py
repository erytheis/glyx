import numpy as np
from scipy.linalg import block_diag
from simulator.servo import *
import math


pos = np.array([0, 0, 0])
servo = Servo(pos, (0, math.pi / 2, 0))

filename = "/Users/erytheis/PycharmProjects/Glyx/simulator/blender_drawer.py"
exec(compile(open(filename).read(), filename, 'exec'))


print(servo.joint_coordinates)
