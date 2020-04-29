#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8

print('robot node is starting...')

# flag
user_flag = -1

def face_cb(msg):
	global count
	print(msg.data)
	if msg.data == 'follow':
		count += 1
		print(count)

def user_cb(msg):
    global user_flag
    print("status : data from user" + str(msg))
    if msg.data == 'user':
        user_flag = 1
    elif msg.data == 'cancel':
        user_flag = 0

rospy.init_node("robot")
rospy.Subscriber("face_status", String,face_cb)
rospy.Subscriber("user_status", String,user_cb)
pub = rospy.Publisher('robot_status',String,queue_size = 1)

count = 0

while not rospy.is_shutdown():

	if user_flag == 0:
		count = 0
		print('status : cancel by user')
		print('status : robot go to check point')
		user_flag = -1

	if count == 30 and user_flag == 1:
		pub.publish('arrived')
		count = 0
		print("status : published 'arrived'")

