#!/usr/bin/env python

import pygame
from pygame.locals import *

import time

import pygame.camera
import Tkinter as Tk
from Tkinter import *
import tkMessageBox

import rospy
from std_msgs.msg import String
#import face_recognition
#import cv2
#import numpy as np

def robot_cb(msg):
    global user_flag
    global arrived_flag
    print("status : " + str(msg.data))
    if msg.data == 'arrived':
        arrived_flag = 1

# initial node
rospy.init_node('navigation_command')
pub = rospy.Publisher('command', String, queue_size = 1)
rospy.Subscriber("robot_status", String, robot_cb)
#pub_cancel = rospy.Publisher('cancel',String,queue_size = 1)
#pub_user = rospy.Publisher('user_status',String,queue_size = 1)
#arrived_robot = rospy.Subscriber("robot_status", String, robot_cb)
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

def button_touch(event,msg,x,y,w,h,color,pic,screen):
    global target
    global flagrun
    screen.blit(pic , (x,y)) # paint to screen
    # in area
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
        if x+w > event.pos[0] > x and y+h > event.pos[1] > y:
            print(msg)
            target = msg
            Tk().wm_withdraw() #to hide the main window
            MsgBox = tkMessageBox.askyesno('Direction dialog','Are you sure you want to go to room ' +msg+ ' ?')
            if MsgBox == TRUE:
                # tkMessageBox.showinfo('Direction','Navigation to room ' + msg)    
                pub.publish(target) ### SEND Room target
                print('published : ' + str(target))
                flagrun = 1
            else:   
               tkMessageBox.showinfo('Return','You will now return to the application screen')
                
    
def button_text(event,msg,x,y,w,h,color,display_surface,pic):
    global target
    global flagrun
    global arrived_robot
    display_surface.blit(pic , (0,0)) # paint to screen
    pygame.draw.rect(display_surface, color,(x,y,w,h))
    # in area
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
        if x+w > event.pos[0] > x and y+h > event.pos[1] > y:
            #print(msg)
            target = msg
            Tk().wm_withdraw() #to hide the main window
            MsgBox = tkMessageBox.askyesno('Direction dialog','Are you sure you want to go to room ' +msg+ ' ?')
            print(MsgBox)
            if MsgBox == TRUE:
                tkMessageBox.showinfo('Direction','Navigation to room ' + msg)
                pub.publish(target) ### SEND CANCEL DATA
                print('published : ' + str(target))
                flagrun = 0
            else:   
                tkMessageBox.showinfo('Return','You will now return to the application screen')
                #time.sleep(5)
                #arrived_robot == 'arrvied'
                flagrun = 1

    smallText = pygame.font.SysFont("comicsansms",30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display_surface.blit(textSurf, textRect)

def update(self):
    if self.hovered:
        self.image = self.image_hovered
    else:
        self.image = self.image_normal
        
def draw(self, surface):
    surface.blit(self.image, self.rect)

def handle_event(self, event):
    if event.type == pygame.MOUSEMOTION:
        self.hovered = self.rect.collidepoint(event.pos)
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if self.hovered:
            print('Clicked:', self.text)
            if self.command:
                self.command()
                
def text_box(msg,x,y,w,h,color):
    global target
    pygame.draw.rect(display_surface, color,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",72)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display_surface.blit(textSurf, textRect)
    
def message_arrived(text, delay,x,y,w,h):
    global flagrun
    global arrived_robot
    smallText = pygame.font.SysFont("comicsansms",30)
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
    arrived_robot = 'A'
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
# path = os.path.join(os.path.expanduser('~'), 'catkin_ws', 'src', 'testnav', 'src')
path = os.path.join(os.path.expanduser('~'), 'test_ws', 'src', 'test_pkg', 'scripts')
display_surface = pygame.display.set_mode((0, 0 ))
pygame.display.set_caption('Image')
image = pygame.image.load(path + '/post_map_.jpg') 
post_sofa=pygame.image.load(path + '/post_sofa_.jpg')
post_refrigerator=pygame.image.load(path + '/post_refrigerator_.jpg')
post_stair=pygame.image.load(path + '/post_stair_.jpg')

# inital text
#font = pygame.font.Font('freesansbold.ttf', 64) 
#text = font.render('Welcome to 11th floor', True, (192, 192,192))

#textRect = text.get_rect()
#textRect.center = (X // 2, Y // 2)

LEFT = 1

running = 1
arrived_robot = 'A'
flagrun = 0
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
    #print(flagrun
        
    if flagrun == 0:
        button_touch(event,"sofa",80,480,240,120,red,post_sofa,display_surface)
        button_touch(event,"center",500,415,210,170,red,post_refrigerator,display_surface)
        button_touch(event,"post_stair",750,150,210,170,red,post_stair,display_surface)
    # show button x,y,w,h

    # elif flagrun == 1 and arrived_flag == 0:
    #     # button_text(event,'cancel',315,350,600,150,green,display_surface,image)
    #     print('status : robot canceled !')
    #     Tk().wm_withdraw() #to hide the main window
    #     MsgBox = tkMessageBox.askyesno('Cancel?')
    #     if MsgBox == TRUE:
    #         pub.publish('cancel') ### SEND CANCEL DATA
    #         print('published : cancel')
    #         flagrun = 0
    #     else:
    #         pass
    
    elif flagrun == 1 and arrived_flag == 1:
        print('status : robot arrvied !')
        Tk().wm_withdraw() #to hide the main window
        MsgBox = tkMessageBox.askyesno('Arrived')
        if MsgBox == TRUE:
            flagrun = 0
        else:
            pass

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