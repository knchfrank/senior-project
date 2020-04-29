#!/usr/bin/env python

# requirement
import rospy
from std_msgs.msg import String
import face_recognition
import cv2
import numpy as np

print('face_recognition node is starting...')

user_flag = 0
arrived_flag = 0

def user_cb(msg):
    global user_flag
    print("status : data from user " + str(msg))
    if msg.data == 'user':
        user_flag = 1
    elif msg.data == 'cancel':
        user_flag = 0

def robot_cb(msg):
    global arrived_flag
    print("status : data from robot" + str(msg))
    if msg.data == 'arrived':
        arrived_flag = 1
    else:
        arrived_flag = 0

# initial node
rospy.init_node('face_recognition')
rospy.Subscriber("user_status", String, user_cb)
rospy.Subscriber("robot_status", String, robot_cb)
pub = rospy.Publisher('face_status',String,queue_size = 1)
rate = rospy.Rate(1)

while not rospy.is_shutdown():
    if user_flag == 1:

        print('status : confirm user, start recognition...')

        # inital face recog
        video_capture = cv2.VideoCapture(0)
        user_image = face_recognition.load_image_file("temp.jpg")
        user_face_encoding = face_recognition.face_encodings(user_image)[0]
        known_face_encodings = [user_face_encoding,]
        known_face_names = ["user",]
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        time = 0

        while not rospy.is_shutdown():
            if user_flag == 0:
                print('status : cancel by user')
                break

            elif cv2.waitKey(1) & 0xFF == ord('q'):
                print('status : cancel by press \'q\'')
                break
            
            elif arrived_flag == 1:
                arrived_flag = 0
                user_flag = 0
                print('status : cancel by robot arrvied')
                break
            
            else:
                # Grab a single frame of video
                ret, frame = video_capture.read()

                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

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
                if not 'user' in face_names:
                    pub.publish("unfollow")
                    print("status : published 'unfollow'")
                else:
                    print("user_flag : " + str(user_flag))
                    pub.publish("follow")
                    print("status : published 'follow'")
                
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
                cv2.imshow('Video', frame)

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
    else:
        pass