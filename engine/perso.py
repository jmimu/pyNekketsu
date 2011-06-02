#! /usr/bin/python


import pygame
import os
import random
from sprite import Sprite

class Perso(Sprite):
    
    def __init__(self):
        Sprite.__init__(self)
        self.pos=[random.randint(-80, 80),random.randint(-40, 40),2]
        self.anim_index=0
        self.direction=1# +1: right, -1: left
        self.state="walk"
        self.has_ball=0 #the ball if is in "hands"
        
        self.jump_speed = 0
        
        self.anim={}#dictionnary for left and right
        self.anim[1]={} #dictionnary of all animation looking to the right
        self.anim[1]["walk"]=[]
        self.anim[1]["walk"].append(pygame.image.load("data/walk_A.png"))
        self.anim[1]["walk"].append(pygame.image.load("data/walk_B.png"))
        self.anim[1]["walk"].append(pygame.image.load("data/walk_C.png"))
        self.anim[1]["walk"].append(pygame.image.load("data/walk_D.png"))
        self.anim[1]["jump"]=[]
        self.anim[1]["jump"].append(pygame.image.load("data/jump_A.png"))
        self.anim[1]["jump"].append(pygame.image.load("data/jump_B.png"))
        
        #flip all anims to look left
        self.anim[-1]={}
        for key in self.anim[1]:
            self.anim[-1][key]=[]
            for img in self.anim[1][key]:
                self.anim[-1][key].append(pygame.transform.flip(img, 1, 0))
        
        
        self.image = self.anim[self.direction][self.state][int(self.anim_index)] #this is how we get the current picture
        
        
    def update(self,inputs,field):
         # Increase the y position by the jump speed
        self.pos[2] += self.jump_speed
        self.jump_speed -= 0.4
        
        if (self.jump_speed < -0.5):
            self.state="jump"
            self.anim_index=1
        field.collide_with_player(self)
        

