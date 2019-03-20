"""
Example of how bodies interact with each other. For a body to be able to
move it needs to have joints. In this example, the "robot" is a red ball
with X and Y slide joints (and a Z slide joint that isn't controlled).
On the floor, there's a cylinder with X and Y slide joints, so it can
be pushed around with the robot. There's also a box without joints. Since
the box doesn't have joints, it's fixed and can't be pushed around.
"""
from mujoco_py import load_model_from_xml, MjSim, MjViewer
import math
import os
from simulator.servo import Servo
from simulator.view.xml_builder import *
import numpy as np



# Initializing servos
coordinates = np.array([0, 0, 0])
servo1 = Servo(coordinates, (0, 0, 0), 0)
servo2 = Servo(coordinates, (0, 0, 0), 0)
servo3 = Servo(coordinates, (0, 0, 0), 0)

# Joint connecting the servos
servo2.join_servo(servo1, 1)
servo3.join_servo(servo2, 1)


# Building the xml
builder = xml_builder()
worldbody = builder.worldbody
append_servo(worldbody, servo1)
append_servo(worldbody, servo2)
append_servo(worldbody, servo3)
TEST_XML = str(builder.get_root_str())[2:-1]



# Building the model
model = load_model_from_xml(TEST_XML)
sim = MjSim(model)
viewer = MjViewer(sim)
t = 0
while True:
    t += 1
    sim.step()
    viewer.render()
    if t > 100 and os.getenv('TESTING') is not None:
        break
