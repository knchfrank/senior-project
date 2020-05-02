#!/usr/bin/env python

import pygame
from pygame.locals import *

import time

import pygame.camera


#import rospy
#from std_msgs.msg import String
#import face_recognition
#import cv2
#import numpy as np

def robot_cb(msg):
    global user_flag
    global arrived_flag
    #print("status : data from robot" + str(msg))
    if msg.data == 'arrived':
        arrived_flag = 1
        
def user_cb(status):
    global user_flag
    global arrived_flag
    if status.data == 'not_found':
        user_flag = 1
    elif status.data == 'not_found_end':
        user_flag = 2

# initial node


#rospy.init_node('navigation_command')
#pub = rospy.Publisher('command', String, queue_size = 1)
#rospy.Subscriber("robot_status", String, robot_cb)
#rospy.Subscriber("user_status", String, user_cb)
#rate = rospy.Rate(1)

# def capture_user():
#     global capture_flag
#     global user
#     filename = 'temp.jpg'
#     #cam.start()
#     #image = cam.get_image()
#     #pygame.image.save(image, filename)
#     #cam.stop()
#     capture_flag = 1

#     # find face
#     image = face_recognition.load_image_file("temp.jpg")
#     face_locations = face_recognition.face_locations(image)
#     if(face_locations):
#         print("status : captured " + str(filename) + " found face at " + str(face_locations))
#         user = 'user'
#     else:
#         print("status : captured " + str(filename) + " not found face")
#         user = ''

#     user_image = pygame.image.load('temp.jpg')
#     return user_image

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button_touch(event,msg,x,y,w,h,color,pic,screen):
    global target
    global flagrun
    global flag_yesno
    global flag_cancel
    global flagcheck
    global arrived_flag
    screen.blit(pic , (x,y)) # paint to screen
    # in area
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
        if x+w > event.pos[0] > x and y+h > event.pos[1] > y:
            print(msg)
            target = msg
            flagcheck = 1
               
def button_yesno(event,msg,x,y,w,h,color,display_surface,pic,status):
    global target
    global flagrun
    global flag_yesno
    global flag_cancel
    global flagcheck
    global arrived_flag
    #font = pygame.font.Font('freesansbold.ttf', 64) 
    #text = font.render('Welcome to 11th floor', True, (192, 192,192))

    #textRect = text.get_rect()
    #textRect.center = (X // 2, Y // 2)
    pygame.draw.rect(display_surface, color,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",48)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display_surface.blit(textSurf, textRect)
    #print(msg)
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
        if x+w > event.pos[0] > x and y+h > event.pos[1] > y and status == 'ready':
            #target = msg
            if msg == 'Yes':
                flagrun = 1
                flag_cancel = 0
                flagcheck = 1
                #pub.publish(target) ####################### pub target ###############################
            elif msg == 'No':
                flagrun = 0
                flag_cancel = 0
                flagcheck = 0
        if x+w > event.pos[0] > x and y+h > event.pos[1] > y and status == 'interupt':
            if msg == 'Yes':
                flagrun = 0
                flag_cancel = 0
                flagcheck = 0 
                #pub.publish('cancel') ####################### pub string cancel # string 'cancel' ###############################
            elif msg == 'No':
                flagrun = 1
                flag_cancel = 0
                flagcheck = 1
                #arrived_flag = 1
    
def button_text(event,msg,x,y,w,h,color,display_surface,pic):
    global target
    global flagrun
    global arrived_flag
    global flag_yesno
    global flag_cancel
    display_surface.blit(pic , (0,0)) # paint to screen
    pygame.draw.rect(display_surface, color,(x,y,w,h))
    # in area
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
        if x+w > event.pos[0] > x and y+h > event.pos[1] > y:
            #print(msg)
            flag_cancel = 1
            #target = msg
    smallText = pygame.font.SysFont("comicsansms",48)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display_surface.blit(textSurf, textRect)


                
def text_box(msg,x,y,w,h,color):
    global target
    pygame.draw.rect(display_surface, color,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",60)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display_surface.blit(textSurf, textRect)
    
def message_arrived(text, delay,x,y,w,h):
    global flagrun
    global arrived_flag
    smallText = pygame.font.SysFont("comicsansms",48)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display_surface.fill(white)
    display_surface.blit(textSurf, textRect)
    pygame.display.flip()
    current_time = pygame.time.get_ticks()
    exit_time = current_time + delay
    clock = pygame.time.Clock()
    flagrun = 0
    running = True
    arrived_flag = 0
    while running:
        current_time = pygame.time.get_ticks()
        if current_time >= exit_time:
            running = False
        clock.tick(1)

# flags
capture_flag = 0
target = ''
user = ''
arrived_flag = 0
flagstop =0

# initial
pygame.init()
#pygame.camera.init()
#pygame.display.set_caption('Navigation Robot')

# camera pygame
# cam = pygame.camera.Camera("/dev/video0")

# inital color
black = (0,0,0)
white = (255, 255, 255) 
silver = (192,192,192)
green = (0, 255, 0) 
blue = (0, 0, 128)
red = (128, 0, 0)

# initial surface
X = 1200
Y = 800 
import os
path = os.path.join(os.path.expanduser('~'), 'catkin_ws', 'src', 'testnav', 'src')
display_surface = pygame.display.set_mode((0, 0 ))
pygame.display.set_caption('Image')
image = pygame.image.load(path + '/post_map_.jpg') 
post_sofa=pygame.image.load(path + '/post_sofa_.jpg')
post_refrigerator=pygame.image.load(path + '/post_refrigerator_.jpg')
post_stair=pygame.image.load(path + '/post_stair_.jpg')


# display_surface = pygame.display.set_mode((0, 0 ))
# pygame.display.set_caption('Image') 
# image = pygame.image.load('F:\CPEY.4\PROJECT\GUI\post\post_map_.jpg') 
# post_sofa=pygame.image.load('F:\CPEY.4\PROJECT\GUI\post\post_sofa_.jpg')
# post_refrigerator=pygame.image.load('F:\CPEY.4\PROJECT\GUI\post\post_refrigerator_.jpg')
# post_stair=pygame.image.load('F:\CPEY.4\PROJECT\GUI\post\post_stair_.jpg')

# inital text
#font = pygame.font.Font('freesansbold.ttf', 64) 
#text = font.render('Welcome to 11th floor', True, (192, 192,192))

#textRect = text.get_rect()
#textRect.center = (X // 2, Y // 2)
running = 1
arrived_flag = 0
flag_cancel = 0
flagrun = 0
flag_yesno = 0
flagcheck = 0
user_flag = 0
while running:
    

    # start touch screen polling
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            running = 0

    # show surface
    display_surface.blit(image,(0,0))
    # show welcom
    #display_surface.blit(text, textRect)

    #show default
    if flag_cancel == 0 and flagrun == 0 and arrived_flag == 0 and flagcheck == 0:
        button_touch(event,"sofa",80,480,240,120,red,post_sofa,display_surface)
        button_touch(event,"refrigerator",500,415,210,170,red,post_refrigerator,display_surface)
        button_touch(event,"stair",750,150,210,170,red,post_stair,display_surface)
    #show     
    elif flag_cancel == 0 and flagrun == 0 and arrived_flag == 0 and flagcheck == 1:
        text_box('Do you want to go to '+ target +' ?',50,190,1200,150,silver)
        button_yesno(event,'No',650,350,200,150,red,display_surface,image,'ready')
        button_yesno(event,'Yes',350,350,200,150,green,display_surface,image,'ready')
    elif flagrun == 1 and arrived_flag == 0 and flag_cancel == 0:
        button_text(event,'cancel',315,350,600,150,green,display_surface,image)
    elif flag_cancel == 1 and flagrun == 1 and arrived_flag == 0:
        text_box('Do you want to cancel to '+ target +' ?',50,190,1200,150,silver)
        button_yesno(event,"No",650,350,200,150,red,display_surface,image,'interupt')
        button_yesno(event,'Yes',350,350,200,150,green,display_surface,image,'interupt')

    # show arrived
    if arrived_flag == 1 and flagrun == 1:
        message_arrived("Arrived!", 1000,315,350,600,150)
        arrived_flag = 0
        flag_cancel = 0
        flagrun = 0
        flag_yesno = 0
        flagcheck = 0
        
    # face not found
    if user_flag == 1 and flagrun == 1:
        text_box('User not found Please move closer to camera.',50,190,1200,150,silver)
    # face not found_end    
    if arrived_flag == 0 and flagrun == 1 and user_flag == 2:
        message_arrived("User not found ! reset navigation.", 1000,315,350,600,150)
        arrived_flag = 0
        flag_cancel = 0
        flagrun = 0
        flag_yesno = 0
        flagcheck = 0

    # capture user
    # if target != '':
    #     print(target)
    #     if target == 'cancel':
    #         user = target
    #         pub_user.publish(user)
    #         print("published : '" + str(target) + "' and '" + str(user) + "'")
    #         target = ''
    #         user = ''
    #     else:
    #         print("status : get target is '" + str(target) + "'")
    #         user_image = capture_user()

    #         pub_target.publish(target)
    #         pub_user.publish(user)
    #         print("published : '" + str(target) + "' and '" + str(user) + "'")
    #         target = ''
    #         user = ''

    # # show user face
    # if capture_flag == 1:
    #     user_image = pygame.transform.scale(user_image, (1280 // 8, 720 // 8))
    #     imgRect = user_image.get_rect()
    #     imgRect.center = (X // 2, (Y // 2)-100)
    #     display_surface.blit(user_image,imgRect)



    pygame.display.flip()
    pygame.display.update()