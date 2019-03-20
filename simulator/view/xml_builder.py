from lxml import etree

# create XML
root = etree.Element('root')
root.append(etree.Element('child'))
# another child with text
child = etree.Element('child')
child.text = 'some text'
root.append(child)

# pretty string
s = etree.tostring(root, pretty_print = True)


def create_servo_xml(servo = 0):
    # position = servo.base_coordinates
    # joint_coordinates = servo.joint_coordinates
    position = (0, 0, 0)
    joint_coordinates = (0, 0, 0)

    pos_str = '{:.1f} {:.1f} {:.1f}'.format(position[0],
                                               position[1],
                                               position[2])
    joint_type_str = 'hinge'
    joint_pos_str = '{:.1f} {:.1f} {:.1f}'.format(joint_coordinates[0],
                                                    joint_coordinates[1],
                                                    joint_coordinates[2])
    root = etree.Element('body')
    root.set('pos', pos_str)

    joint_child = etree.Element('joint')
    joint_child.set('type', joint_type_str)
    joint_child.set('pos', joint_pos_str)
    root.append(joint_child)

    res_string = etree.tostring(root, pretty_print = True)
    print(s)
    return res_string, root

_, root = create_servo_xml()


def append_servo(root, servo=0):
    _, child_servo = create_servo_xml()
    root.append(child_servo)
    res_string = etree.tostring(root, pretty_print = True)
    print(res_string)
    return res_string, root

append_servo(root)
