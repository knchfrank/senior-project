#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def robot_cb(status):
    if status.data == 'arrvied':
        print('robot arrvied!')

def user_cb(status):
    if status.data == 'not_found':
        print('not found user!')
    elif status.data == 'not_found_end':
        print('not found user!.....end')

rospy.init_node('navigation_command')
pub = rospy.Publisher('robot_command', String, queue_size = 1)
rospy.Subscriber('robot_status', String, robot_cb)
rospy.Subscriber('user_status', String, user_cb)

while not rospy.is_shutdown():
    msg = raw_input('command (sofa, center, stair, cancel) : ')
    pub.publish(msg)
    print('published : ' + str(msg))