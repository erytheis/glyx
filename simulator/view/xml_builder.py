from lxml import etree
import xml.etree.cElementTree as ET
import sys

class World_body():
    servo_counter = 0

    COMPILER = 'radian'
    BASE_COLOR = '0.8 0 0 .6'
    JOINT_COLOR = '0 0.5 .8 .6'

    def __init__(self):
        root = etree.Element('mujoco')

        # Compiler
        compiler_child = etree.Element('compiler')
        compiler_child.set('angle', 'radian')
        root.append(compiler_child)

        # Worldbody
        worldbody_child = etree.Element('worldbody')
        root.append(worldbody_child)

        self.root = root
        self.worldbody_child = worldbody_child
        self.draw_coordinate_basis()
        self.draw_lights()
        self.draw_plane()

    def append_servo_body(self, servo_body):
        self.worldbody_child.append(servo_body.root)

    def get_root_str(self):
        return str(etree.tostring(self.root))[2:-1]

    def draw_coordinate_basis(self):
        """
        Draw a X,Y,Z reference coordinate basis reperesented as a cylinders
        """
        # Zero point
        origin_site_child = etree.Element('site')
        origin_site_child.set('name', 'base')
        origin_site_child.set('pos', '0 0 0')
        origin_site_child.set('type', 'sphere')
        origin_site_child.set('size', '0.015')
        origin_site_child.set('rgba', '0.8 1 1 1')
        self.worldbody_child.append(origin_site_child)

        # X_axis basis
        x_site_child = etree.Element('site')
        x_site_child.set('name', 'x_axis')
        x_site_child.set('euler', '0 1.57 0')
        x_site_child.set('pos', '0.1 0 0')
        x_site_child.set('type', 'cylinder')
        x_site_child.set('size', '0.01 0.1')
        x_site_child.set('rgba', '1 0 0 1')
        self.worldbody_child.append(x_site_child)

        # Y_axis basis
        y_site_child = etree.Element('site')
        y_site_child.set('name', 'y_axis')
        y_site_child.set('euler', '-1.57 0 0')
        y_site_child.set('pos', '0 0.1 0')
        y_site_child.set('type', 'cylinder')
        y_site_child.set('size', '0.01 0.1')
        y_site_child.set('rgba', '0 1 0 1')
        self.worldbody_child.append(y_site_child)

        # Z_axis basis
        z_site_child = etree.Element('site')
        z_site_child.set('name', 'z_axis')
        z_site_child.set('euler', '0 0 0')
        z_site_child.set('pos', '0 0 0.1')
        z_site_child.set('type', 'cylinder')
        z_site_child.set('size', '0.01 0.1')
        z_site_child.set('rgba', '0 0 1 1')
        self.worldbody_child.append(z_site_child)

    def draw_lights(self):
        light_child = etree.Element('light')
        light_child.set('diffuse', '.5 .5 .5')
        light_child.set('pos', '0 0 3')
        light_child.set('dir', '0 0 -1')
        self.worldbody_child.append(light_child)

    def draw_plane(self):
        # Plane
        geom_child = etree.Element('geom')
        geom_child.set('type', 'plane')
        geom_child.set('size', "1 1 0.1")
        geom_child.set('rgba', ".6 0.6 0.6 1")
        self.worldbody_child.append(geom_child)


def draw_xml_line(child_type_str, **kwargs):
    """
    Create an XML object
    :param root:
    :param kwargs: all parameters presented in Type = "value" format
    :return:
    """
    child = etree.Element(child_type_str)

    if kwargs is not None:
        for key, value in kwargs.items():
            child.set(str(key), value)

    return child


def build_xml_file(root):
    mydata = str(etree.tostring(root))[2:-1]
    myfile = open("worldbody.xml", "w")
    myfile.write(mydata)
