#!/usr/bin/env python

import rospy
import numpy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler

# initial node
pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
rospy.init_node('send_goal')

# define parameter
p = PoseStamped()
p.header.seq = 0
p.header.stamp = rospy.Time.now()
p.header.frame_id = 'map'

p.pose.position.x = 12.23
p.pose.position.y = -0.56
p.pose.position.z = 0.0

p.pose.orientation.x = 0.0
p.pose.orientation.y = 0.0
p.pose.orientation.z = 1.0
p.pose.orientation.w = 0.0

# publlish to topic
pub.publish(p)

rospy.spin()