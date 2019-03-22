from simulator.physics import rotate_vector_euler, get_orientation_from_vectors
import math
import numpy as np
from quaternion import from_euler_angles, rotate_vectors, as_quat_array

SIDES = np.array([.1, .2, .2])
JOINT_RELATIVE_COORDINATES = np.array([0., -.1, .4])
JOINT_OFFSET = np.array([0., 0., SIDES[0]])
DEFAULT_ORIENTATION_TOP = [0, 0, 1]
DEFAULT_ORIENTATION_FRONT = [1, 0, 0]
DEFAULT_ORIENTATION_SIDE = [0, 1, 0]


class Servo():
    def __init__(self, coordinates = (0, 0, 0), euler = (0, 0, 0), position = 0,
                 quaternion = None):
        # TODO rename coordinates into relative position
        self.base_coordinates = np.asanyarray(coordinates)
        self.euler = np.asanyarray(euler)
        self.position = position

        self.quaternion = quaternion
        if quaternion == None:
            self.quaternion = from_euler_angles(self.euler)

        self.angular_speed = 0

        # Finding orientation vectors
        self.orientation_vector_x = np.asanyarray(rotate_vectors(self.quaternion, DEFAULT_ORIENTATION_FRONT))
        self.orientation_vector_y = np.asanyarray(rotate_vectors(self.quaternion, DEFAULT_ORIENTATION_SIDE))
        self.orientation_vector_z = np.asanyarray(rotate_vectors(self.quaternion, DEFAULT_ORIENTATION_TOP))

        self.joined_servo_rotation_quaternion = as_quat_array(
            np.insert((self.orientation_vector_y * math.sin(math.pi / 4)), 0, - math.sin(math.pi / 4)))

        # Calculate coordinates of a joint
        self.update_joint_coordinates()

    def attach_to_servo(self, other_servo):
        """
        connects THIS servo to OTHER servo, translating the base coordinates of THIS servo
        to the coordinates of the joint of the OTHER servo.
        :param other_servo:
        :param connected_side: 1 or -1 means the direction of the rotation
        :return:
        """
        self.connected_servo = other_servo

        offset = rotate_vectors(other_servo.quaternion, JOINT_OFFSET)
        self.base_coordinates = other_servo.joint_coordinates + offset
        print(self.base_coordinates)

        self.set_quaternion(other_servo.joined_servo_rotation_quaternion)
        self.update_joint_coordinates()

    def update_joint_coordinates(self):
        self.joint_coordinates = self.base_coordinates + rotate_vectors(self.quaternion,
                                                                        JOINT_RELATIVE_COORDINATES)

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
        self.euler = self.connected_servo.orientation
        self.euler[0] += self.connected_servo.connected_side * self.connected_servo.position
        self.update_joint_coordinates(self.euler)
        # Turn the engine
        self.position += self.angular_speed

    def set_euler(self, orientation):
        self.euler = orientation
        self.orientation_vector_z = rotate_vector_euler(DEFAULT_ORIENTATION_TOP, self.euler)

    def set_quaternion(self, quaternion):
        self.quaternion = quaternion

        # Update all the orientation vectors
        self.orientation_vector_x = np.asanyarray(rotate_vectors(self.quaternion, DEFAULT_ORIENTATION_FRONT))
        self.orientation_vector_y = np.asanyarray(rotate_vectors(self.quaternion, DEFAULT_ORIENTATION_SIDE))
        self.orientation_vector_z = np.asanyarray(rotate_vectors(self.quaternion, DEFAULT_ORIENTATION_TOP))
