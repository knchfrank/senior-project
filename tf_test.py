#!/usr/bin/env python

import math
import rospy
import tf
import time
from tf.transformations import quaternion_from_euler as qfe
from geometry_msgs.msg import Twist

vx= 0
wz=0

br = tf.TransformBroadcaster()

def kk_cb(msg):
    global vx,wz
    vx = msg.linear.x
    wz = msg.angular.z

rospy.init_node("Leang")
rospy.Subscriber("cmd_vel",Twist,kk_cb)
rate = rospy.Rate(10)

x=0
y=0
lx=0
ly=0
th = 0

ltime = rospy.Time.now()
while not rospy.is_shutdown():
    now = rospy.Time.now()
    #dt = (now-ltime).to_sec()
    #x += vx*math.cos(th)*dt
    #y += vx*math.sin(th)*dt
    #th += wz*dt
    x = math.cos(now.to_sec())
    y = math.sin(now.to_sec())
    br.sendTransform((x,y,0),qfe(0,0,0),now,"robot","map") #x,y,z #timberlock #(0,0,0,1) quaternion
    lx=x
    ly=y
    #x += 0.01
    #y += 0.01
    rate.sleep()
    ltime = now
