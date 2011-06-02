#! /usr/bin/python


import pygame
import os

from sprite import Sprite

class Ball(Sprite):
    
    def __init__(self):
        Sprite.__init__(self)

        self.speed=[4,3,8]
        self.owner=0 #0 if bass is free

        self.anim_index=0
        self.direction=1# +1: right, -1: left  TODO : add more directions ?
        self.state="roll1"
        
        self.anim={}#dictionnary for left and right
        self.anim[1]={} #dictionnary of all animation looking to the right
        self.anim[1]["roll1"]=[]
        self.anim[1]["roll1"].append(pygame.image.load("data/_ball_roll1_A.png"))
        self.anim[1]["roll1"].append(pygame.image.load("data/_ball_roll1_B.png"))
        self.anim[1]["roll1"].append(pygame.image.load("data/_ball_roll1_C.png"))
        self.anim[1]["roll1"].append(pygame.image.load("data/_ball_roll1_D.png"))
        self.anim[1]["roll1"].append(pygame.image.load("data/_ball_roll1_E.png"))
        self.anim[1]["roll1"].append(pygame.image.load("data/_ball_roll1_F.png"))
        
        #flip all anims to look left
        self.anim[-1]={}
        for key in self.anim[1]:
            self.anim[-1][key]=[]
            for img in self.anim[1][key]:
                self.anim[-1][key].append(pygame.transform.flip(img, 1, 0))
        
        self.image = self.anim[self.direction][self.state][int(self.anim_index)] #this is how we get the current picture
        
        
    def update(self,field):
        if (self.owner!=0):
            self.speed[0]=(self.owner.pos[0]+4*self.owner.direction-self.pos[0])*4
            self.speed[1]=(self.owner.pos[1]-self.pos[1])*4

        if (abs(self.speed[0])<0.2):
            self.speed[0]=0
        if (abs(self.speed[1])<0.2):
            self.speed[1]=0
 
        self.pos[0]+=self.speed[0]*0.2
        self.pos[1]+=self.speed[1]*0.2
        self.pos[2]+=self.speed[2]*0.2
        self.speed[2]+=-2*0.2

   

        #bounce
        if (self.pos[2] <= field.z):
            self.pos[2] = field.z
            self.speed[2]=abs(self.speed[2])*field.bounce_damp
            if (abs(self.speed[2])<1.0):
                self.speed[2]=0
 
       
        # Keep in bounds
        if self.pos[0] < -field.half_length:
            self.pos[0] = -field.half_length
            self.speed[0]*=-0.8
        if self.pos[0] > field.half_length:
            self.pos[0] = field.half_length
            self.speed[0]*=-0.8
        if self.pos[1] < -field.half_width:
            self.pos[1] = -field.half_width
            self.speed[1]*=-0.8
        if self.pos[1] > field.half_width:
            self.pos[1] = field.half_width
            self.speed[1]*=-0.8


        self.direction=1
        if (self.speed[0]<0):
            self.direction=-1
        
        self.anim_index += (self.speed[0]**2+self.speed[1]**2)/50.0

        if (self.anim_index>=len(self.anim[self.direction][self.state])):
            self.anim_index=0
        self.image = self.anim[self.direction][self.state][int(self.anim_index)]
        
