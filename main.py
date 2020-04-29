#!/usr/bin/env python

import pygame
from pygame.locals import *

import pygame.camera

import rospy
from std_msgs.msg import String
import face_recognition
import cv2
import numpy as np

def robot_cb(msg):
    global user_flag
    global arrived_flag
    print("status : data from robot" + str(msg))
    if msg.data == 'arrived':
        arrived_flag = 1

# initial node
rospy.init_node('user_interface')
pub_target = rospy.Publisher('target',String,queue_size = 1)
pub_user = rospy.Publisher('user_status',String,queue_size = 1)
rospy.Subscriber("robot_status", String, robot_cb)
rate = rospy.Rate(1)

def capture_user():
    global capture_flag
    global user
    filename = 'temp.jpg'
    cam.start()
    image = cam.get_image()
    pygame.image.save(image, filename)
    cam.stop()
    capture_flag = 1

    # find face
    image = face_recognition.load_image_file("temp.jpg")
    face_locations = face_recognition.face_locations(image)
    if(face_locations):
        print("status : captured " + str(filename) + " found face at " + str(face_locations))
        user = 'user'
    else:
        print("status : captured " + str(filename) + " not found face")
        user = ''

    user_image = pygame.image.load('temp.jpg')
    return user_image

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button_mouse(msg,x,y,w,h,ic,ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # in area
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(display_surface, ac,(x,y,w,h))
        if click[0] == 1:
            print(msg)
    else:
        pygame.draw.rect(display_surface, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display_surface.blit(textSurf, textRect)

def button_touch(event,msg,x,y,w,h,color):
    global target
    pygame.draw.rect(display_surface, color,(x,y,w,h))

    # in area
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
        if x+w > event.pos[0] > x and y+h > event.pos[1] > y:
            # print(msg)
            target = msg

    smallText = pygame.font.SysFont("comicsansms",30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display_surface.blit(textSurf, textRect)

def text_box(msg,x,y,w,h,color):
    global target
    pygame.draw.rect(display_surface, color,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display_surface.blit(textSurf, textRect)

# flags
capture_flag = 0
target = ''
user = ''
arrived_flag = 0

# initial
pygame.init()
pygame.camera.init()
pygame.display.set_caption('Navigation Robot')

# camera pygame
cam = pygame.camera.Camera("/dev/video0")

# inital color
black = (0,0,0)
white = (255, 255, 255) 
silver = (192,192,192)
green = (0, 255, 0) 
blue = (0, 0, 128)
red = (128, 0, 0)

# initial surface
X = 400
Y = 400 
display_surface = pygame.display.set_mode((X, Y ))

# inital text
font = pygame.font.Font('freesansbold.ttf', 32) 
text = font.render('welcome', True, green, blue)
textRect = text.get_rect()
textRect.center = (X // 2, Y // 2)

LEFT = 1

running = 1

while running:

    # start touch screen polling
    event = pygame.event.poll()
    if event.type == pygame.QUIT or rospy.is_shutdown():
        running = 0

    # show surface
    display_surface.fill(white)

    # show welcom
    display_surface.blit(text, textRect)

    # show button x,y,w,h
    button_touch(event,"1115",10,10,60,30,silver)
    button_touch(event,"1121",10,50,60,30,silver)
    button_touch(event,"toilet",10,90,60,30,silver)
    button_touch(event,"cancel",10,130,60,30,red)

    # capture user
    if target != '':
        print(target)
        if target == 'cancel':
            user = target
            pub_user.publish(user)
            print("published : '" + str(target) + "' and '" + str(user) + "'")
            target = ''
            user = ''
        else:
            print("status : get target is '" + str(target) + "'")
            user_image = capture_user()

            pub_target.publish(target)
            pub_user.publish(user)
            print("published : '" + str(target) + "' and '" + str(user) + "'")
            target = ''
            user = ''

    # show user face
    if capture_flag == 1:
        user_image = pygame.transform.scale(user_image, (1280 // 8, 720 // 8))
        imgRect = user_image.get_rect()
        imgRect.center = (X // 2, (Y // 2)-100)
        display_surface.blit(user_image,imgRect)

    # show arrived
    if arrived_flag == 1:
        arrived_flag = 0
        print('status : robot arrvied !')

    # event = pygame.event.poll()
    # if event.type == pygame.QUIT:
    #     running = 0
    # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
    #     print("You pressed the left mouse button at (%d, %d)" % event.pos)
    #     print(event.pos[0])
    # elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
    #     print("You released the left mouse button at (%d, %d)" % event.pos)

    pygame.display.flip()