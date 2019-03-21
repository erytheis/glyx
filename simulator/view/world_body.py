from lxml import etree
from simulator.servo import SIDES

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

        # Lightitng
        light_child = etree.Element('light')
        light_child.set('diffuse', '.5 .5 .5')
        light_child.set('pos', '0 0 3')
        light_child.set('dir', '0 0 -1')
        worldbody_child.append(light_child)

        # Plane
        geom_child = etree.Element('geom')
        geom_child.set('type', 'plane')
        geom_child.set('size', "1 1 0.1")
        geom_child.set('rgba', ".6 0.6 0.6 1")
        worldbody_child.append(geom_child)

        # Zero point
        origin_site_child = etree.Element('site')
        origin_site_child.set('name', 'base')
        origin_site_child.set('pos', '0 0 0')
        origin_site_child.set('type', 'sphere')
        origin_site_child.set('size', '0.015')
        origin_site_child.set('rgba', '0.8 1 1 1')
        worldbody_child.append(origin_site_child)

        # X_axis basis
        x_site_child = etree.Element('site')
        x_site_child.set('name', 'x_axis')
        x_site_child.set('euler', '0 1.57 0')
        x_site_child.set('pos', '0.1 0 0')
        x_site_child.set('type', 'cylinder')
        x_site_child.set('size', '0.01 0.1')
        x_site_child.set('rgba', '1 0 0 1')
        worldbody_child.append(x_site_child)

        # Y_axis basis
        y_site_child = etree.Element('site')
        y_site_child.set('name', 'y_axis')
        y_site_child.set('euler', '-1.57 0 0')
        y_site_child.set('pos', '0 0.1 0')
        y_site_child.set('type', 'cylinder')
        y_site_child.set('size', '0.01 0.1')
        y_site_child.set('rgba', '0 1 0 1')
        worldbody_child.append(y_site_child)

        # Z_axis basis
        z_site_child = etree.Element('site')
        z_site_child.set('name', 'z_axis')
        z_site_child.set('euler', '0 0 0')
        z_site_child.set('pos', '0 0 0.1')
        z_site_child.set('type', 'cylinder')
        z_site_child.set('size', '0.01 0.1')
        z_site_child.set('rgba', '0 0 1 1')
        worldbody_child.append(z_site_child)


        self.root = root
        self.worldbody_child = worldbody_child

    def append_servo_body(self, servo_body):
        self.worldbody_child.append(servo_body.root)

    def get_root_str(self):
        return etree.tostring(self.root)



class Servo_body():

    def __init__(self, servo):

        # Initialization of variables
        self.geom_color_str = '0 .9 0 .5'
        self.size = SIDES
        self.servo_object = servo
        self.euler = '0 0 0'

        # Initialization of strings
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

        # Building an xml
        self.create_servo_xml()


    def create_servo_xml(self):
        """
        Building a XML element describing the servo
        :param servo:
        :return: string of a xml, root object of lxml
        """
        World_body.servo_counter += 1

        # Initializing roots
        root = etree.Element('body')
        root.set('pos', self.pos_str)

        # Geom parameters
        geom_child = etree.Element('geom')
        geom_child.set('pos', self.pos_str)
        geom_child.set('type', 'box')
        geom_child.set('size', self.geom_size_str)
        geom_child.set('rgba', self.geom_color_str)
        geom_child.set('name', self.geom_name_str)
        root.append(geom_child)

        # Joint parameters
        joint_child = etree.Element('joint')
        joint_child.set('type', self.joint_type_str)
        joint_child.set('pos', self.joint_pos_str)
        root.append(joint_child)


        # Join site parameters
        joint_site_child = etree.Element('site')
        joint_site_child.set('name', self.site_name_str)
        joint_site_child.set('pos', self.joint_pos_str)
        joint_site_child.set('type', 'sphere')
        joint_site_child.set('size', self.sphere_size_str)
        joint_site_child.set('rgba', World_body.JOINT_COLOR)
        root.append(joint_site_child)


        # Origin site parameters
        base_site_child = etree.Element('site')
        base_site_child.set('name', self.pos_name_str)
        base_site_child.set('pos', self.pos_str)
        base_site_child.set('type', 'sphere')
        base_site_child.set('size', self.sphere_size_str)
        base_site_child.set('rgba', World_body.BASE_COLOR)
        root.append(base_site_child)


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

