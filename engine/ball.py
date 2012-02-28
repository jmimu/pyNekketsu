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
import math
from settings import configuration

from sprite import Sprite


class Ball(Sprite):
    snd_bounce = pygame.mixer.Sound("data/sound/etw/shoot2.wav")
    def __init__(self):
        Sprite.__init__(self)
        self.pos=[0,0,15] #like every other thing, pos is at center bottom

        self.speed=[0,20,10]
        self.size=2 #ball radius, for goal accuracy (used in y, and 2* in z)
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
                if (configuration["sound"]=="on"):
                    Ball.snd_bounce.play()
        
        # Keep in bounds if match not finished
        if (match.match_time>0):
            if self.pos[0] < -match.field.half_length:
                self.pos[0] = -match.field.half_length
                self.speed[0]*=-0.8
                if (configuration["game_mode"]!="fight") and (abs(self.pos[1]-match.field.goal_latitude[-1])<match.field.goal_half_width[-1]-self.size) \
                    and (self.pos[2]<match.field.z+match.field.goal_height[-1]-self.size*2):#goal!
                    match.team[1].nb_goals+=1
                    if (self.owner!=0):
                        self.owner.has_ball=0
                        self.owner=0
                    self.pos[2]=35
                    self.speed[:]=[6,random.randint(-6,6),6]
                    print("Score: %d - %d"%(match.team[-1].nb_goals,match.team[1].nb_goals))
                    if (configuration["sound"]=="on"):
                        match.snd_whistle.play()
                    match.goaldrawing_time=20
                else:
                    if (configuration["sound"]=="on"):
                        Ball.snd_bounce.play()
            if self.pos[0] > match.field.half_length:
                self.pos[0] = match.field.half_length
                self.speed[0]*=-0.8
                if (configuration["game_mode"]!="fight") and (abs(self.pos[1]-match.field.goal_latitude[1])<match.field.goal_half_width[1]-self.size) \
                    and (self.pos[2]<match.field.z+match.field.goal_height[1]-self.size*2):#goal!
                    match.team[-1].nb_goals+=1
                    if (self.owner!=0):
                        self.owner.has_ball=0
                        self.owner=0
                    self.pos[2]=35
                    self.speed[:]=[-6,random.randint(-6,6),6]
                    print("Score: %d - %d"%(match.team[-1].nb_goals,match.team[1].nb_goals))
                    if (configuration["sound"]=="on"):
                        match.snd_whistle.play()
                    match.goaldrawing_time=20
                else:
                    if (configuration["sound"]=="on"):
                        Ball.snd_bounce.play()
            if self.pos[1] < -match.field.half_width:
                self.pos[1] = -match.field.half_width
                self.speed[1]*=-0.8
                if (configuration["sound"]=="on"):
                    Ball.snd_bounce.play()
            if self.pos[1] > match.field.half_width:
                self.pos[1] = match.field.half_width
                self.speed[1]*=-0.8
                if (configuration["sound"]=="on"):
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
        
    #bounce on a circle
    #return false if not possible to bounce
    def bounce_on_player(self,pl):
        ball_radius=2
        player_radius=3
        if not(((self.pos[0]-pl.pos[0])**2+(self.pos[1]-pl.pos[1])**2)<(ball_radius+player_radius)**2):
            return False#no collision
        #find ball position where contact begins (with ball speed)
        contact_pos_x=0
        contact_pos_y=0
        #equation: contact_pos=l*vit_ball+ball_pos     and    dist(contact_pos-player_pos)=5
        a=self.speed[0]
        b=self.speed[1]
        c=self.pos[0]-pl.pos[0]
        d=self.pos[1]-pl.pos[1]
        dist2=(ball_radius+player_radius)**2
        #(l*a+c)**2+(l*b+d)**2=dist2
        delta=(2*a*c+2*b*d)**2-4*(a**2+b**2)*(c**2+d**2-dist2)
        if (delta<0): #there is no contact point
            return False
        solution1=(-2*a*c-2*b*d+math.sqrt(delta))/(2*a**2+2*b**2)
        solution2=(-2*a*c-2*b*d-math.sqrt(delta))/(2*a**2+2*b**2)
        l=solution1
        if (solution2<=0):
            l=solution2
        if (l>0):
            #there is no contact in the past
            return False
#        print("previous_pos: ",self.pos[0],self.pos[1],(pl.pos[0]-self.pos[0])**2+(pl.pos[1]-self.pos[1])**2)
        self.pos[0]+=l*self.speed[0]
        self.pos[1]+=l*self.speed[1]
#        print("new_pos: ",self.pos[0],self.pos[1],(pl.pos[0]-self.pos[0])**2+(pl.pos[1]-self.pos[1])**2)
        #mirror the ball velocity
        
        c=self.pos[0]-pl.pos[0]#vector from ball to player
        d=self.pos[1]-pl.pos[1]
        norm=math.sqrt(c**2+d**2)
        scal_product=(self.speed[0]*c+self.speed[1]*d)/norm
#        print("for scal_product ",self.speed[0],c,self.speed[1],d,norm)
        v_a_x=c*scal_product/norm
        v_a_y=d*scal_product/norm

#        print(c,d,"   scal ",scal_product)
#        print(self.speed[0],self.speed[1],v_a_x,v_a_y)
#        print("speed before: ",self.speed[0],self.speed[1],math.sqrt(self.speed[0]**2+self.speed[1]**2))
        self.speed[0]-=2*v_a_x
        self.speed[1]-=2*v_a_y
#        print("final ",self.speed[0],self.speed[1])
#        print("speed after: ",self.speed[0],self.speed[1],math.sqrt(self.speed[0]**2+self.speed[1]**2))
        #slow down ball
        self.speed[0]*=0.6
        self.speed[1]*=0.6
        return True

