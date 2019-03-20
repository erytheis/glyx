from lxml import etree


class xml_builder():
    servo_counter = 0

    COLORS = '0 .9 0 .8'
    SIZE = '.2 .2 .1'
    COMPILER = 'radian'

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
        geom_child.set('rgba', ".9 0 0 1")
        worldbody_child.append(geom_child)

        self.root = root
        self.worldbody = worldbody_child

    def get_root_str(self):
        return etree.tostring(self.root)


def create_servo_xml(servo):
    """
    Building a XML element describing the servo
    :param servo:
    :return: string of a xml, root object of lxml
    """
    position = servo.base_coordinates
    joint_coordinates = servo.joint_coordinates
    xml_builder.servo_counter += 1

    # Initialization of strings
    pos_str = '{:.1f} {:.1f} {:.1f}'.format(position[0],
                                            position[1],
                                            position[2])
    joint_type_str = 'hinge'
    joint_pos_str = '{:.1f} {:.1f} {:.1f}'.format(joint_coordinates[0],
                                                  joint_coordinates[1],
                                                  joint_coordinates[2])
    site_name_str = 'end' + str(xml_builder.servo_counter)
    site_size_str = '0.01'

    geom_name_str = 'servo' + str(xml_builder.servo_counter)

    # Initializing roots
    root = etree.Element('body')
    root.set('pos', pos_str)

    # Joint parameters
    joint_child = etree.Element('joint')
    joint_child.set('type', joint_type_str)
    joint_child.set('pos', joint_pos_str)
    root.append(joint_child)

    # Geom parameters
    geom_child = etree.Element('geom')
    geom_child.set('type', 'box')
    geom_child.set('size', xml_builder.SIZE)
    geom_child.set('rgba', xml_builder.COLORS)
    geom_child.set('name', geom_name_str)
    root.append(geom_child)

    # Site parameters
    site_child = etree.Element('site')
    site_child.set('name', site_name_str)
    site_child.set('pos', joint_pos_str)
    site_child.set('type', 'sphere')
    site_child.set('size', site_size_str)
    root.append(site_child)

    res_string = etree.tostring(root, pretty_print = True)

    return res_string, root


def append_servo(root, new_servo):
    """
    :param root:
    :param new_servo:
    :return: string of a xml, root object of lxml
    """
    _, child_servo = create_servo_xml(new_servo)
    root.append(child_servo)
    res_string = etree.tostring(root, pretty_print = True)
    return res_string, root




