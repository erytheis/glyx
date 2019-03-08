from simulator.physics import rotate_vector
import math
import numpy as np

joint_relative_coordinates = np.array([- 0.005, - 0.005, 0.015])


class Servo():
    def __init__(self, coordinates = (0, 0, 0), orientation = (0, 0, 0), position = 0):
        self.base_coordinates = coordinates
        self.orientation = np.asanyarray(orientation)
        self.width = 0.02
        self.height = 0.02
        self.body_is_rotating = False
        self.update_joint_coordinates(self.orientation)
        self.angular_speed = 0
        self.position = position

    def join_servo(self, other_servo, connected_side):
        """
        connects THIS servo to OTHER servo, translating the base coordinates of this servo
        to the coordinates of the joint of the other servo.
        :param other_servo:
        :param connected_side: 1 or -1
        :return:
        """
        self.connected_side = connected_side
        self.connected_servo = other_servo
        self.base_coordinates = other_servo.joint_coordinates
        self.orientation = other_servo.orientation + (0, math.pi / 2, math.pi / 2)
        self.update_joint_coordinates(self.orientation)
        print(self.base_coordinates)
        print(self.orientation)

    def update_joint_coordinates(self, orientation):
        self.joint_coordinates = rotate_vector(self.base_coordinates + joint_relative_coordinates, orientation)

    def set_angular_speed(self, w):
        self.angular_speed = w

    def update(self):
        """

        :return:
        """
        self.connected_servo.update()
        # Relative translative motion
        self.base_coordinates = self.connected_servo.joint_pos
        # Relative rotative motion
        self.orientation = self.connected_servo.orientation
        self.orientation[0] += self.connected_servo.connected_side * self.connected_servo.position
        self.update_joint_coordinates(self.orientation)
        # Turn the engine
        self.position += self.angular_speed
