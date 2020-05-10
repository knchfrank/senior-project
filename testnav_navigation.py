#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

command = ''
rospy.init_node('movebase_client_py')
pub = rospy.Publisher('robot_status', String, queue_size = 1)
client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
client.wait_for_server()

def command_callback(msg):
    global client
    global command
    command = msg.data
    print('received from robot_command : ' + str(command))
    if command == 'cancel':
        client.cancel_goal()
        command = ''

def result_callback(msg):
    print('received from move_base/result status : ' + str(msg.status.status))
    if msg.status.status == 2:  # moving -> cancel
        rospy.loginfo("canceled")
        pass
    elif msg.status.status == 3: # arrived
        pub.publish('arrived')
        print('published : arrived')
    elif msg.status.status == 4: # ready state, fail -> cancel
        print('fail')


def goto(client, command):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    if command == 'sofa':

        goal.target_pose.pose.position.x = 2.8409
        goal.target_pose.pose.position.y = -0.0746
        goal.target_pose.pose.position.z = 0.0

        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0

    elif command == 'center' or command == 'refrigerator':
        
        goal.target_pose.pose.position.x = -0.1504
        goal.target_pose.pose.position.y = -0.0175
        goal.target_pose.pose.position.z = 0.0

        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0
    
    elif command == 'stair':
        
        goal.target_pose.pose.position.x = -0.3377
        goal.target_pose.pose.position.y = -1.5967
        goal.target_pose.pose.position.z = 0.0

        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 0.7050

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

rospy.Subscriber("robot_command", String, command_callback)
rospy.Subscriber("move_base/result", String, result_callback)

print('Ready to get command.')

while not rospy.is_shutdown():
    # status = client.get_state()
    # print(status)
    if command != '':
        result = goto(client, command)
        if result:
            rospy.loginfo("Execution done! " + str(command))
        command = ''