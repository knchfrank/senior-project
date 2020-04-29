#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32

def kk_cb(msg):
	print(msg.data)

rospy.init_node("Listen_node")
rospy.Subscriber("test_float_publish",Float32,kk_cb)

rospy.spin()
