#! /usr/bin/python
# -*- coding: utf-8 -*-

#    pyNekketsu
#    Copyright (C) 2011  JM Muller
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import pygame
import os
import random

from sprite import Sprite


class Ball(Sprite):
    snd_bounce = pygame.mixer.Sound("data/sound/etw/shoot2.wav")
    def __init__(self):
        Sprite.__init__(self)
        self.pos=[0,0,15] #like every other thing, pos is at center bottom

        self.speed=[0,20,10]
        self.size=1 #ball radius, for goal accuracy (used in y, and 2* in z)
        self.owner=0 #0 if ball is free

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
        
        
    def update(self,match):
        
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
        if (self.pos[2] <= match.field.z):
            self.pos[2] = match.field.z
            self.speed[2]=abs(self.speed[2])*match.field.bounce_damp
            self.speed[0]=self.speed[0]*match.field.roll_damp
            self.speed[1]=self.speed[1]*match.field.roll_damp
            if (self.speed[2]<1.5):
                self.speed[2]=0
            else:
                self.speed[0]=self.speed[0]*match.field.roll_damp#damp is stronger if rebounce
                self.speed[1]=self.speed[1]*match.field.roll_damp
                Ball.snd_bounce.play()
        
        # Keep in bounds if match not finished
        if (match.match_time>0):
            if self.pos[0] < -match.field.half_length:
                self.pos[0] = -match.field.half_length
                self.speed[0]*=-0.8
                if (abs(self.pos[1]-match.field.goal_latitude[-1])<match.field.goal_half_width[-1]-self.size) \
                    and (self.pos[2]<match.field.z+match.field.goal_height[-1]-self.size*2):#goal!
                    match.team[1].nb_goals+=1
                    if (self.owner!=0):
                        self.owner.has_ball=0
                        self.owner=0
                    self.pos[2]=35
                    self.speed[:]=[6,random.randint(-6,6),6]
                    print("Score: %d - %d"%(match.team[-1].nb_goals,match.team[1].nb_goals))
                    match.snd_whistle.play()
                    match.goaldrawing_time=20
                else:
                    Ball.snd_bounce.play()
            if self.pos[0] > match.field.half_length:
                self.pos[0] = match.field.half_length
                self.speed[0]*=-0.8
                if (abs(self.pos[1]-match.field.goal_latitude[1])<match.field.goal_half_width[1]-self.size) \
                    and (self.pos[2]<match.field.z+match.field.goal_height[1]-self.size*2):#goal!
                    match.team[-1].nb_goals+=1
                    if (self.owner!=0):
                        self.owner.has_ball=0
                        self.owner=0
                    self.pos[2]=35
                    self.speed[:]=[-6,random.randint(-6,6),6]
                    print("Score: %d - %d"%(match.team[-1].nb_goals,match.team[1].nb_goals))
                    match.snd_whistle.play()
                    match.goaldrawing_time=20
                else:
                    Ball.snd_bounce.play()
            if self.pos[1] < -match.field.half_width:
                self.pos[1] = -match.field.half_width
                self.speed[1]*=-0.8
                Ball.snd_bounce.play()
            if self.pos[1] > match.field.half_width:
                self.pos[1] = match.field.half_width
                self.speed[1]*=-0.8
                Ball.snd_bounce.play()
            
        
        self.direction=1
        if (self.speed[0]<0):
            self.direction=-1
        
        self.animation()

    def animation(self):
        self.anim_index += (self.speed[0]**2+self.speed[1]**2)/50.0

        if (self.anim_index>=len(self.anim[self.direction][self.state])):
            self.anim_index=0
        self.image = self.anim[self.direction][self.state][int(self.anim_index)]
        
