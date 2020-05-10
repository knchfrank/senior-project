#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import face_recognition
import cv2
import numpy as np
import os

# callback
user_status = 'empty'
user_command = 'empty'
robot_status = 'empty'
def user_cb(msg):
    global user_command
    user_command = msg.data # target or cancel
    print('received from command : ' + str(user_command))
    if user_command == 'cancel':
        pub_to_robot.publish('cancel')

def robot_cb(msg):
    global robot_status
    robot_status = msg.data # target or cance
    print('received from robot_status : ' + str(robot_status))

# initial node
rospy.init_node('face_recognition')
rospy.Subscriber("command", String, user_cb)
rospy.Subscriber("robot_status", String, robot_cb)
pub_to_user = rospy.Publisher('user_status',String,queue_size = 1)
pub_to_robot = rospy.Publisher('robot_command',String,queue_size = 1)
rate = rospy.Rate(1)

def recognition():
    global user_command
    global robot_status

    # inital face recog
    video_capture = cv2.VideoCapture(0)
    path = "/home"
    # user_image = face_recognition.load_image_file(os.path.join(path, "post/test_ws/src/test_pkg/scripts", "temp2.jpg"))
    user_image = face_recognition.load_image_file(os.path.join(path, "pi/catkin_ws/src/testnav/src", "temp2.jpg"))
    user_face_encoding = face_recognition.face_encodings(user_image)[0]
    known_face_encodings = [user_face_encoding,]
    known_face_names = ["user",]
    face_locations = []
    face_encodings = []
    face_names = []
    last_time_found = rospy.Time.now()
    process_this_frame = True
    published_goal = 0
    published_cancel = 0
    published_found = 0
    while not rospy.is_shutdown():
        if user_command == 'cancel' or robot_status == 'arrived':
            print('user_command : ' + str(user_command) + ', robot_status : ' + str(robot_status))
            if user_command == 'cancel':
                pub_to_robot.publish('cancel')
                pub_to_user.publish('cancel')
            break  

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.255)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            # face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=0, model="cnn")
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
        
        if 'user' in face_names:
            last_time_found = rospy.Time.now()
            time_lost = 0
            published_cancel = 0
            if not published_goal:
                pub_to_robot.publish(user_command)
                pub_to_user.publish('found')
                print('published to robot : ' + str(user_command) + ', published to user : found')
                published_goal = 1
            # if not published_found:
            #     pub_to_user.publish('found')
            #     print('published to robot : cancel, published to user : found')
            #     published_found = 1
        else:
            time_lost = rospy.Time.now() - last_time_found

            if time_lost.secs != 0:
                print('lost user : ' + str(time_lost.secs) + 's')
            
            if time_lost.secs > 5:  # total time lost 
                pub_to_robot.publish('center')
                pub_to_user.publish('not_found_end')
                print('published to robot : cancel, published to user : not_found_end')
                break
            if time_lost.secs > 1:    # little bit time lost
                if not published_cancel:
                    pub_to_robot.publish('cancel')
                    pub_to_user.publish('not_found')
                    print('published to robot : cancel, published to user : not_found')
                    published_goal = 0
                    published_cancel = 1
                    published_found = 0
            else:
                pass



        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        # cv2.imshow('Video', frame)
    
    video_capture.release()
    cv2.destroyAllWindows()

def print_all_flag():
    global user_command
    global user_status
    global robot_status
    print('user_command' + ' : ' + str(user_command))
    print('user_status' + ' : ' + str(user_status))
    print('robot_status' + ' : ' + str(robot_status))

print('ready to get command...')
while not rospy.is_shutdown():
    if user_command != 'empty' and user_command != 'cancel':
        print('start recognition...')
        recognition()
        print('end recognition...')
        user_status = 'empty'
        user_command = 'empty'
        robot_status = 'empty'
        print_all_flag()
    else:
        pass