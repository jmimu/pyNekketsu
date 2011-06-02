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
        self.anim[1]["shoot"]=[]
        self.anim[1]["shoot"].append(pygame.image.load("data/shoot_A.png"))
        self.anim[1]["shoot"].append(pygame.image.load("data/shoot_B.png"))
        self.anim[1]["shoot"].append(pygame.image.load("data/shoot_C.png"))
        self.anim[1]["attack"]=[]
        self.anim[1]["attack"].append(pygame.image.load("data/attack_A.png"))
        self.anim[1]["hurt"]=[]
        self.anim[1]["hurt"].append(pygame.image.load("data/hurt_A.png"))
        
        #flip all anims to look left
        self.anim[-1]={}
        for key in self.anim[1]:
            self.anim[-1][key]=[]
            for img in self.anim[1][key]:
                self.anim[-1][key].append(pygame.transform.flip(img, 1, 0))
        
        
        self.image = self.anim[self.direction][self.state][int(self.anim_index)] #this is how we get the current picture
        
        
    def update(self,match):
        self.previous_pos[:]=self.pos[:]
         # Increase the y position by the jump speed
        self.pos[2] += self.jump_speed
        self.jump_speed -= 0.4
        
        if (self.jump_speed < -0.5):
            self.state="jump"
            self.anim_index=1


        if (self.state=="shoot"):
            self.anim_index += 0.2
            if (self.anim_index>=len(self.anim[self.direction][self.state])):
                self.anim_index=0
                self.state="walk"
        if (self.state=="attack"):
            self.anim_index += 0.1
            self.pos[0]+=self.direction/5.0
            if (self.anim_index>=len(self.anim[self.direction][self.state])):
                self.anim_index=0
                self.state="walk"
        if (self.state=="hurt"):
            self.anim_index += 0.05
            self.pos[0]-=self.direction/10.0
            if (self.anim_index>=len(self.anim[self.direction][self.state])):
                self.anim_index=0
                self.state="walk"
            
        #try to catch the ball 
        if (self.state=="walk") and (match.ball.owner==0):
            if (0<(match.ball.pos[0]-self.pos[0])*self.direction<4) \
                and (abs(match.ball.pos[1]-self.pos[1])<5) \
                and (abs(match.ball.pos[2]-self.pos[2])<5):
                match.ball.owner=self
                self.has_ball=match.ball
                match.ball.speed=[0,0,0]
            

        #update animation
        if (self.anim_index>=len(self.anim[self.direction][self.state])):
            self.anim_index=0
        self.image = self.anim[self.direction][self.state][int(self.anim_index)]
 

        match.field.collide_with_player(self)



    def shoot(self,match):
        if (match.ball.owner==0) or (self.has_ball==0):
            print("Error on shoot!")
            match.ball.owner=0
            self.has_ball=0
            return

        self.state="shoot"
        self.anim_index=0

        match.ball.speed[0]=(self.pos[0]-self.previous_pos[0])*5 + 5*self.direction
        match.ball.speed[1]=(self.pos[1]-self.previous_pos[1])*5
        match.ball.speed[2]=5

        match.ball.owner=0
        self.has_ball=0


    def attack(self,match):
        self.state="attack"
        self.anim_index=0

        for p in match.perso_list:
            if (p!=self):
                if (0<(p.pos[0]-self.pos[0])*self.direction<6) \
                    and (abs(p.pos[1]-self.pos[1])<5) \
                    and (abs(p.pos[2]-self.pos[2])<5):
                    #p is attacked !
                    p.state="hurt"
                    p.anim_index=0
                    p.direction=-self.direction
                    if (p.has_ball != 0):
                        p.has_ball=0
                        match.ball.owner=0
                        match.ball.speed[0]+=5*self.direction

