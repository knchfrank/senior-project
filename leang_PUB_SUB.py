#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16

def kk_cb(msg):
    a = Int16()
    a.data = msg.data + 5
    pub_int.publish(a)
	#print(msg.data)

pub_int = rospy.Publisher('C',Int16,queue_size = 1)
rospy.init_node('Leang_ja')
print('Hi_leang')

rospy.Subscriber("A",Int16,kk_cb)
rospy.spin()

#rate = rospy.Rate(10)

# count = 0
# a = Int16()
# while not rospy.is_shutdown():
# 	a.data = count
# 	count += 1
# 	if(count == 127):
# 		count = 0
# 	pub_int.publish(a)	
# 	pub.publish("hello")
# 	rate.sleep()

