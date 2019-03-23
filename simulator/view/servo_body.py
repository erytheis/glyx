from lxml import etree
from quaternion import as_float_array

from simulator.servo import SIDES
from simulator.view.xml_builder import World_body, draw_xml_line


class Servo_body():

    def __init__(self, servo):
        # Initialization of variables
        self.geom_color_str = '0 .9 0 .5'
        self.size = SIDES
        self.servo_object = servo

        # Building an xml
        self.initialize_string()
        self.create_servo_xml()

    def initialize_string(self):
        """
        Initialize string, that are used in XML builder
        :return:
        """
        self.position = self.servo_object.base_coordinates
        self.joint_coordinates = self.servo_object.joint_coordinates

        self.pos_str = '{:.2f} {:.2f} {:.2f}'.format(self.position[0],
                                                     self.position[1],
                                                     self.position[2])
        self.pos_name_str = 'base' + str(World_body.servo_counter)

        self.joint_type_str = 'hinge'
        self.joint_pos_str = '{:.2f} {:.2f} {:.2f}'.format(self.joint_coordinates[0],
                                                           self.joint_coordinates[1],
                                                           self.joint_coordinates[2])

        self.site_name_str = 'end' + str(World_body.servo_counter)
        self.sphere_size_str = '0.01'

        self.geom_name_str = 'servo' + str(World_body.servo_counter)
        self.geom_size_str = '{:.2f} {:.2f} {:.2f}'.format(self.size[0],
                                                           self.size[1],
                                                           self.size[2])

        self.quaternion = as_float_array(self.servo_object.quaternion)
        self.quaternion_str = '{:.3f} {:.3f} {:.3f} {:.3f}'.format(self.quaternion[0],
                                                                   self.quaternion[1],
                                                                   self.quaternion[2],
                                                                   self.quaternion[3])

    def create_servo_xml(self):
        # TODO build an XML files for readability
        """
        Building a XML element describing the servo
        :param servo:
        :return: string of a xml, root object of lxml
        """
        World_body.servo_counter += 1

        # Initializing roots
        root = etree.Element('body')
        # root.set('pos', self.pos_str)
        geom_child = draw_xml_line(root, 'geom', pos = self.pos_str, type = 'box', size = self.geom_size_str,
                                   rgba = self.geom_color_str, name = self.geom_name_str, quat = self.quaternion_str)

        # Joint parameters
        joint_child = draw_xml_line(root, 'joint', type = self.joint_type_str, pos = self.joint_pos_str)

        # Join site parameters
        joint_site_child = draw_xml_line(root, 'site', name = self.site_name_str, pos = self.joint_pos_str,
                                         type = 'sphere',
                                         size = self.sphere_size_str, rgba = World_body.JOINT_COLOR)

        # Origin site parameters
        base_site_child = draw_xml_line(root, 'site', name = self.pos_name_str, pos = self.pos_str, type = 'sphere',
                                        size = self.sphere_size_str, rgba = World_body.BASE_COLOR)

        # Append children
        root.append(geom_child)
        root.append(joint_child)
        root.append(base_site_child)
        root.append(joint_site_child)

        res_string = etree.tostring(root, pretty_print = True)

        self.root = root
        self.geom_child = geom_child
        self.joint_site_child = joint_site_child

        return res_string, root


    def append_servo_body(self, new_servo_body):
        """
        Attach a new servo to an existing servo as a xml child
        :param new_servo_body:
        :return: string of a resulted xml, root object of base servo lxml
        """
        _, child_servo = new_servo_body.create_servo_xml()
        self.root.append(child_servo)
        res_string = etree.tostring(self.root, pretty_print = True)
        return res_string, self.root


    def set_geom_color(self, color):
        """
        :param color: an array of size 4 with rgba elements
        """
        self.color = color
        self.geom_color_str = '{:.2f} {:.2f} {:.2f} {:.2f}'.format(color[0],
                                                                   color[1],
                                                                   color[2],
                                                                   color[3])
        self.geom_child.set('rgba', self.geom_color_str)


    def set_position(self, position):
        self.position = position
        self.pos_str = '{:.2f} {:.2f} {:.2f}'.format(self.position[0],
                                                     self.position[1],
                                                     self.position[2])
