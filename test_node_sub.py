#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def kk_cb(msg):
	print(msg.data)

rospy.init_node("Listen_node")
rospy.Subscriber("test_topic",String,kk_cb)

rospy.spin()
