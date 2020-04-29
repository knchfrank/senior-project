#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8

pub = rospy.Publisher('test_topic',String,queue_size = 1)
pub_int = rospy.Publisher('test_topic_int',Int8,queue_size = 1)
rospy.init_node('node_name_ja')
print('Hi')

rate = rospy.Rate(10)
count = 0
a = Int8()
while not rospy.is_shutdown():
	a.data = count
	count += 1
	if(count == 127):
		count = 0
	pub_int.publish(a)	
	pub.publish("hello")
	rate.sleep()

