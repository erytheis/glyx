from mujoco_py import load_model_from_xml, MjSim, MjViewer
import os
from simulator.servo import Servo
from simulator.view.servo_body import Servo_body
from simulator.view.xml_builder import *

# Initializing servos
servo1 = Servo(coordinates = (0, 0, 0.5))
servo2 = Servo(coordinates = (0, 0, 0))
# servo3 = Servo(coordinates = (0, 0, 0))

# Joint connecting the servos
servo2.attach_to_servo(servo1)
# servo3.join_servo(servo2, 1)

# Building the world
worldbody = World_body()
servo1_body = Servo_body(servo1)
servo2_body = Servo_body(servo2)
servo1_body.append_servo_body(servo2_body)
worldbody.append_servo_body(servo1_body)
build_xml_file(worldbody.root)

TEST_XML = worldbody.get_root_str()


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


