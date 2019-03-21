from simulator.physics import rotate_vector, DEFAULT_ORIENTATION, get_orientation_from_vectors
import math
import numpy as np

JOINT_RELATIVE_COORDINATES = np.array([0., -.1, .4])
SIDES = np.array([.1, .2, .2])


class Servo():
    def __init__(self, coordinates = (0, 0, 0), orientation = (0, 0, 0), position = 0):
        # TODO rename coordinates into relative position
        self.base_coordinates = coordinates
        self.orientation = np.asanyarray(orientation)
        self.orientation_vector = rotate_vector(DEFAULT_ORIENTATION, self.orientation)
        self.body_is_rotating = False
        self.update_joint_coordinates()
        self.angular_speed = 0
        self.position = position
        self.SIDE = 1

    def join_servo(self, other_servo, connected_side):
        """
        connects THIS servo to OTHER servo, translating the base coordinates of THIS servo
        to the coordinates of the joint of the OTHER servo.
        :param other_servo:
        :param connected_side: 1 or -1 means the direction of the rotation
        :return:
        """
        self.connected_side = connected_side
        self.connected_servo = other_servo
        self.base_coordinates = other_servo.joint_coordinates
        self.orientation_vector = rotate_vector(self.connected_servo.orientation_vector, (0, math.pi / 2, math.pi / 2))
        print(self.orientation_vector)
        new_orientation = get_orientation_from_vectors(DEFAULT_ORIENTATION, self.orientation_vector)
        print(new_orientation)
        self.set_orientation(new_orientation)
        print(self.orientation_vector)
        print()
        self.update_joint_coordinates()

    def update_joint_coordinates(self):
        self.joint_coordinates = self.base_coordinates + rotate_vector(JOINT_RELATIVE_COORDINATES, self.orientation)
        print(self.joint_coordinates)
        print(self.base_coordinates)

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

    def set_orientation(self, orientation):
        self.orientation = orientation
        self.orientation_vector = rotate_vector(DEFAULT_ORIENTATION, self.orientation)
