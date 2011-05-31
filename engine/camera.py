#! /usr/bin/python

import pygame,sys

from pygame.locals import *

#to draw everything in field world, with a projection

class Camera():
    def __init__(self):
        self.x=0.0#camera position
        self.y=-100.0
        self.z=0.0
        self.f=500.0#camera focale
        self.l=20#120 #center of the screen, or less to fake a little tilt
        self.c=128 #center of the screen
        self.decal_to_target=[0,-150,50]
    def aim_to(self,ground_pos,direction,speed=100): # try to go closer to ground_pos point, and look forward in a direction , at a given speed (in %)
        self.decal_to_target[0]=25.0*direction#add to x
        self.x+=(ground_pos[0]+self.decal_to_target[0]-self.x)*speed/100.0
        self.y+=(ground_pos[1]+self.decal_to_target[1]-self.y)*speed/100.0
        self.z+=(ground_pos[2]+self.decal_to_target[2]-self.z)*speed/100.0
        if (self.x<-80):
            self.x=-80
        if (self.x>80):
            self.x=80
    def proj(self,ground_pos,sprite_w=0,sprite_h=0):#ground_pos is a 3D vector
        px=ground_pos[0]-self.x
        py=ground_pos[1]-self.y
        pz=ground_pos[2]-self.z
        pc=px/py*self.f+self.c  -sprite_w/2
        pl=-pz/py*self.f+self.l  -sprite_h
        screen_pos=[pc,pl]
        return screen_pos

