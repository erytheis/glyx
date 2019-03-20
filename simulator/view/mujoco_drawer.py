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
import numpy as np



# Initializing servos
coordinates = np.array([0, 0, 0])
servo1 = Servo(coordinates, (0, 0, 0), 0)
servo2 = Servo(coordinates, (0, 0, 0), 0)
servo3 = Servo(coordinates, (0, 0, 0), 0)

# Joint connecting the servos
servo2.join_servo(servo1, 1)
servo3.join_servo(servo2, 1)



MODEL_XML = """
<mujoco>
 <compiler angle="radian"/>
   <worldbody>
      <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>    
      <geom type="plane" size="1 1 0.1" rgba=".9 0 0 1"/>        
            <body>
            <geom type="capsule" fromto = "0.3 0 1.8  0.3 0 1.2" size="0.04" rgba="0.2 0.2 0.2 0.5"/>
            <joint type="hinge" pos="0.3 0 1.8" axis="0 1 0"/>      
            <joint type="hinge" pos="0.3 0 1.8" axis="1 0 0"/>   
            <joint type="hinge" pos="0.3 0 1.8" axis="0 0 1"/>      
            <site name="end2" pos="0.3 0 1.8" type="sphere" size="0.01"/>
                <body pos="0 0 0">
                <joint type="ball" pos="0.0 0 0"/>
                <site name="end1" pos="0.0 0 0.6" type="sphere" size="0.01"/>
                <geom type="box" size=".2 .2 .1" rgba="0 .9 0 .8" euler = "0 1.57 0"/>
                </body>
            </body>
   </worldbody>
</mujoco>
"""

model = load_model_from_xml(MODEL_XML)
sim = MjSim(model)
viewer = MjViewer(sim)
t = 0
while True:
    t += 1
    sim.step()
    viewer.render()
    if t > 100 and os.getenv('TESTING') is not None:
        break
