#! /usr/bin/python

import pygame,sys

from pygame.locals import *

#to draw everything in field world, with a projection

class Camera():
    def __init__(self):
        self.x=0#camera position
        self.y=0
        self.z=0
        self.l=120 #center of the screen
        self.c=128 #center of the screen
    def project(self,ground_pos):#ground pos is a vector in 3d
        px=ground_pos[0]-self.x
        py=ground_pos[1]-self.y
        pz=ground_pos[2]-self.z
        pc=px*(1000.0+px)/1000+self.c #column
        pl=py/10+pz+self.l #line
        screen_pos=[pc,pl]
        return screen_pos

