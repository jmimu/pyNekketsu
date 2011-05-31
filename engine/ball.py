#! /usr/bin/python


import pygame
import os


class Ball(object):
    
    def __init__(self):
        self.images=[]
        self.image=0
        self.anim_index=0
        self.direction=1# +1: right, -1: left
        self.state="roll1"
        
        self.pos = [0, 0, 2]
        
        self.anim={}#dictionnary for left and right
        self.anim[1]={} #dictionnary of all animation looking to the right
        self.anim[1]["roll1"]=[]
        self.anim[1]["roll1"].append(pygame.image.load("data/ball_roll1_A.png"))
        self.anim[1]["roll1"].append(pygame.image.load("data/ball_roll1_B.png"))
        self.anim[1]["roll1"].append(pygame.image.load("data/ball_roll1_C.png"))
        self.anim[1]["roll1"].append(pygame.image.load("data/ball_roll1_D.png"))
        
        #flip all anims to look left
        self.anim[-1]={}
        for key in self.anim[1]:
            self.anim[-1][key]=[]
            for img in self.anim[1][key]:
                self.anim[-1][key].append(pygame.transform.flip(img, 1, 0))
        
        self.image = self.anim[self.direction][self.state][int(self.anim_index)] #this is how we get the current picture
        
        
    def update(self,inputs):
        self.anim_index += 0.2
        
        if (self.anim_index>=len(self.anim[self.direction][self.state])):
            self.anim_index=0
        self.image = self.anim[self.direction][self.state][int(self.anim_index)]
        
