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
from sprite import compileimage
from inputs import Inputs

class Perso(Sprite):
    
    def __init__(self, team, head):
        Sprite.__init__(self)
        self.team=team
        self.inputs=0 #class Inputs, constructor differs if PersoCPU or PersoPlayer
        self.pos=[random.randint(-80, 80),random.randint(-40, 40),2]
        self.anim_index=0
        self.direction=1# +1: right, -1: left
        self.state="walk"
        self.has_ball=0 #the ball if is in "hands"
        
        self.jump_speed = 0

        self.anim={}#dictionnary for left and right
        self.anim[1]={} #dictionnary of all animation looking to the right
        self.anim[1]["walk"]=[]
        self.anim[1]["walk"].append(compileimage(self.team.number,"walk_A.png",head,"normal.png",(2,0)))
        self.anim[1]["walk"].append(compileimage(self.team.number,"walk_B.png",head,"normal.png",(2,0)))
        self.anim[1]["walk"].append(compileimage(self.team.number,"walk_C.png",head,"normal.png",(2,0)))
        self.anim[1]["walk"].append(compileimage(self.team.number,"walk_D.png",head,"normal.png",(2,0)))
        self.anim[1]["jump"]=[]
        self.anim[1]["jump"].append(compileimage(self.team.number,"jump_A.png",head,"normal.png",(2,0)))
        self.anim[1]["jump"].append(compileimage(self.team.number,"jump_A.png",head,"normal.png",(2,0)))
        self.anim[1]["shoot"]=[]
        self.anim[1]["shoot"].append(compileimage(self.team.number,"shoot_A.png",head,"back.png",(14,0)))
        self.anim[1]["shoot"].append(compileimage(self.team.number,"shoot_B.png",head,"normal.png",(6,1)))
        self.anim[1]["shoot"].append(compileimage(self.team.number,"shoot_C.png",head,"normal.png",(6,0)))
        self.anim[1]["attack"]=[]
        self.anim[1]["attack"].append(compileimage(self.team.number,"attack_A.png",head,"angry.png",(9,1)))
        self.anim[1]["hurt"]=[]
        self.anim[1]["hurt"].append(compileimage(self.team.number,"hurt_A.png",head,"hurt.png",(1,1)))
        
        #flip all anims to look left
        self.anim[-1]={}
        for key in self.anim[1]:
            self.anim[-1][key]=[]
            for img in self.anim[1][key]:
                self.anim[-1][key].append(pygame.transform.flip(img, 1, 0))
        
        
        self.image = self.anim[self.direction][self.state][int(self.anim_index)] #this is how we get the current picture
        
        
    def update(self,match):

        self.handle_inputs(match)


        if (self.state=="jump"): #if jumping, continue to go in previous direction
            jump_speed_x=(self.pos[0]-self.previous_pos[0])
            jump_speed_y=(self.pos[1]-self.previous_pos[1])
            self.pos[0]+=jump_speed_x
            self.pos[1]+=jump_speed_y
            self.previous_pos[0]+=jump_speed_x
            self.previous_pos[1]+=jump_speed_y
        else:
            self.previous_pos[:]=self.pos[:] #be careful with that...
        
        
        
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
            
        #try to catch the ball  : see perso_GK and perso_non_GK
                

        #update animation
        if (self.anim_index>=len(self.anim[self.direction][self.state])):
            self.anim_index=0
        self.image = self.anim[self.direction][self.state][int(self.anim_index)]
    
    
        match.field.collide_with_player(self)
    
    def draw(self,surface,camera,is_shadow=True):
        Sprite.draw(self,surface,camera,is_shadow)
        surface.blit(self.team.image, camera.proj([self.pos[0],self.pos[1],self.pos[2]],self.team.image.get_width(),self.team.image.get_height()*3))
    
    def shoot(self,match):
        if (match.ball.owner==0) or (self.has_ball==0):
            print("Error on shoot!")
            match.ball.owner=0
            self.has_ball=0
            return

        self.state="shoot"
        self.anim_index=0

        match.ball.speed[0]=(self.pos[0]-self.previous_pos[0])*5 + 6*self.direction
        match.ball.speed[1]=(self.pos[1]-self.previous_pos[1])*8
        match.ball.speed[2]=6-(self.pos[0]-self.previous_pos[0])*3

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

    def handle_inputs(self,match):
        if (self.state=="walk"):
            if (self.has_ball!=0):
                if self.inputs.L:
                    self.pos[0] -= 1
                    self.direction = -1
                if self.inputs.R:
                    self.pos[0] += 1
                    self.direction = +1
                if self.inputs.U:
                    self.pos[1] += 1
                if self.inputs.D:
                    self.pos[1] -= 1
            else:#don't have ball
                if self.inputs.L:
                    self.pos[0] -= 1.2
                    self.direction = -1
                if self.inputs.R:
                    self.pos[0] += 1.2
                    self.direction = +1
                if self.inputs.U:
                    self.pos[1] += 1.2
                if self.inputs.D:
                    self.pos[1] -= 1.2
            if (self.inputs.L or self.inputs.R or self.inputs.U or self.inputs.D):
                self.anim_index += 0.2
            # Jump if the player presses the A button
            if (self.inputs.C and self.pos[2] == 0):
                self.jump_speed = 2.5
                self.state="jump"
                self.anim_index=0
                
            if (self.inputs.B):
                if (self.has_ball!=0):
                    self.shoot(match)
            if (self.inputs.A):
                if (self.has_ball==0):
                    self.attack(match)
            
        self.inputs.update() #read the new keys or clear inputs for CPU



