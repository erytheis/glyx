"""
This file is designed in order to print the result in Blender 3D workspace
"""
import numpy as np
import math
import bpy
import sys
import os
import bmesh

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
    width = 0.01
    vertices = [(0, -1, 0.5),
                (-1, -1, 0.5),
                (-1, 1, 0.5),
                (0, 1, 0.5),
                (0, -1, -1.5),
                (-1, -1, -1.5),
                (-1, 1, -1.5),
                (0, 1, -1.5)]
    vertices = [rotate_vector(vert + Servo.base_coordinates, Servo.orientation) * width for vert in vertices]
    print(vertices)
    return vertices


"""
Here the BLENDER drawing code starts
"""

faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]

coordinates = np.array([0, 0, 0])
zero_servo = Servo(coordinates, (0, 0, 0), 0)
first_servo = Servo(coordinates, (0, 0, 0), 0)
second_servo = Servo(coordinates, (0, 0, 0), 0)
first_servo.join_servo(second_servo, 1)
zero_servo.join_servo(first_servo, 1)

verts1 = get_vertices(first_servo)
verts2 = get_vertices(second_servo)
verts3 = get_vertices(zero_servo)

mymesh = bpy.data.meshes.new("Servo")
myobject = bpy.data.objects.new("Servo", mymesh)

mymesh2 = bpy.data.meshes.new("Other servo")
myobject2 = bpy.data.objects.new("Other servo", mymesh2)

mymesh3 = bpy.data.meshes.new("Other servo")
myobject3 = bpy.data.objects.new("Third servo", mymesh3)

myobject.location = first_servo.base_coordinates
bpy.context.scene.objects.link(myobject)

myobject2.location = second_servo.base_coordinates
bpy.context.scene.objects.link(myobject2)

myobject3.location = zero_servo.base_coordinates
bpy.context.scene.objects.link(myobject3)

mymesh.from_pydata(verts1, [], faces)
mymesh.update(calc_edges = True)

mymesh2.from_pydata(verts2, [], faces)
mymesh2.update(calc_edges = True)

mymesh3.from_pydata(verts3, [], faces)
mymesh3.update(calc_edges = True)

# joint coordinates
mesh = bpy.data.meshes.new('second_joint')
basic_sphere = bpy.data.objects.new("second_joint", mesh)
bpy.context.scene.objects.link(basic_sphere)
bm = bmesh.new()
basic_sphere.location = first_servo.joint_coordinates
bmesh.ops.create_uvsphere(bm, u_segments = 32, v_segments = 16, diameter = 0.0001)
bm.to_mesh(mesh)
bm.free()
