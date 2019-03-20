"""
This file is designed in order to print the result in Blender 3D workspace
"""
import numpy as np
import math
import bpy
import sys
import os
import bmesh

# Preparation for integration with blender
blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)
else:
    print("blend dir already in sys")

from simulator.physics import rotate_vector
from simulator.servo import Servo

import importlib

importlib.reload(sys.modules['simulator.servo'])
importlib.reload(sys.modules['simulator.physics'])


def get_vertices(Servo):
    """
    Getting the coordinates of the servo, given that the position of the servo is the joint point to the other base
    servo
    :param Servo:
    :return:
    """
    vertices = [(0, -1, 0.5),
                (-1, -1, 0.5),
                (-1, 1, 0.5),
                (0, 1, 0.5),
                (0, -1, -1.5),
                (-1, -1, -1.5),
                (-1, 1, -1.5),
                (0, 1, -1.5)]
    vertices = [(rotate_vector(vert, Servo.orientation) + Servo.base_coordinates) * Servo.SIDE for vert in vertices]

    return vertices


"""
Here the BLENDER drawing code starts
"""
# filename = "/Users/erytheis/PycharmProjects/Glyx/simulator/blender_drawer.py"
# exec(compile(open(filename).read(), filename, 'exec'))


def clear_scene():
    """
    Clear objects present in the scene
    :return:
    """
    # gather list of items of interest.
    candidate_list = [item.name for item in bpy.data.objects if item.type == "MESH"]
    # select them only.
    for object_name in candidate_list:
        bpy.data.objects[object_name].select = True
    # remove all selected.
    bpy.ops.object.delete()
    # remove the meshes, they have no users anymore.
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)


def draw_servo(servo):
    draw_servo.counter += 1
    verts = get_vertices(servo)
    name = "Servo #" + str(draw_servo.counter)
    mymesh = bpy.data.meshes.new(name)
    myobject = bpy.data.objects.new(name, mymesh)
    myobject.location = (0, 0, 0)
    bpy.context.scene.objects.link(myobject)
    mymesh.from_pydata(verts, [], faces)
    mymesh.update(calc_edges = True)


draw_servo.counter = 0

clear_scene()

# Initializing servos
faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
coordinates = np.array([0, 0, 0])
servo1 = Servo(coordinates, (0, 0, 0), 0)
servo2 = Servo(coordinates, (0, 0, 0), 0)
servo3 = Servo(coordinates, (0, 0, 0), 0)

# Joint connecting the servos
servo2.join_servo(servo1, 1)
servo3.join_servo(servo2, 1)

# Visualizing servos
draw_servo(servo1)
draw_servo(servo2)
draw_servo(servo3)

# joint coordinates
mesh = bpy.data.meshes.new('second_joint')
basic_sphere = bpy.data.objects.new("second_joint", mesh)
bpy.context.scene.objects.link(basic_sphere)
bm = bmesh.new()
basic_sphere.location = servo2.joint_coordinates
bmesh.ops.create_uvsphere(bm, u_segments = 32, v_segments = 16, diameter = 0.0001)
bm.to_mesh(mesh)
bm.free()
