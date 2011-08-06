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
from sprite import Sprite
from sprite import compileimage
from inputs import Inputs

class Player(Sprite):
    snd_pass = pygame.mixer.Sound("data/sound/etw/pass.wav")
    snd_shoot = pygame.mixer.Sound("data/sound/etw/shot.wav")
    snd_attack = pygame.mixer.Sound("data/sound/stk/parachute.wav")
    
    #  pos_init is "expanded" to the whole field with field_half_length
    def __init__(self, team):
        Sprite.__init__(self)
        self.team=team
        self.number_human_player=0
        self.image=0#current image
        #player characteristics
        self.pos_ref=[]#reference position in west half field
        self.pos_aim=[]#in full field coords, (scaled depending on ball position) (not used by GK)
        self.pos=[] #current position
        self.speed=1
        self.health=100
        self.max_energy=1000 #before speed decreases
        self.resistance=1 #before going KO
        self.control=1 #before being hurt by ball
        self.kick=1 #for shooting
        self.punch=1 #for attacking
        self.jump_hight=1 
        #IA characteristics
        self.agressivity=1 
        self.precision=1 #for GK and pass
        self.listening=1 #when asked for pass (max:2)
        
        self.inputs=0 #class Inputs, constructor differs if Player_CPU or Player_Human
        self.anim_index=0
        self.direction=1# +1: right, -1: left
        self.state="walk"
        self.has_ball=0 #the ball if is in "hands"
        self.dist2_to_ball=0 #square of planar dist to ball
        
        self.jump_speed = 0
        self.energy=self.max_energy

        self.anim={}#dictionnary for left and right
        
    def read_xml(self,player_node,field):
        self.name=player_node.getElementsByTagName('name')[0].childNodes[0].data
        self.head_number=int(player_node.getElementsByTagName('head_number')[0].childNodes[0].data)
        #init pos are given in % of field size in xml file
        x_ini=float(player_node.getElementsByTagName('init_pos')[0].getElementsByTagName('x')[0].childNodes[0].data)
        y_ini=float(player_node.getElementsByTagName('init_pos')[0].getElementsByTagName('y')[0].childNodes[0].data)
        #print("Found a player: ",self.name,x_ini,y_ini)
        self.speed=float(player_node.getElementsByTagName('speed')[0].childNodes[0].data)
        self.health=float(player_node.getElementsByTagName('health')[0].childNodes[0].data)
        self.max_energy=float(player_node.getElementsByTagName('max_energy')[0].childNodes[0].data)
        self.resistance=float(player_node.getElementsByTagName('resistance')[0].childNodes[0].data)
        self.control=float(player_node.getElementsByTagName('control')[0].childNodes[0].data)
        self.kick=float(player_node.getElementsByTagName('kick')[0].childNodes[0].data)
        self.punch=float(player_node.getElementsByTagName('punch')[0].childNodes[0].data)
        self.jump_hight=float(player_node.getElementsByTagName('jump_hight')[0].childNodes[0].data) 
        self.agressivity=float(player_node.getElementsByTagName('agressivity')[0].childNodes[0].data)
        self.precision=float(player_node.getElementsByTagName('precision')[0].childNodes[0].data)
        self.listening=float(player_node.getElementsByTagName('listening')[0].childNodes[0].data)
        
        x_ini=-((x_ini-100)/100.0*field.half_length)
        y_ini=(y_ini-50)/100.0*field.half_width
        self.pos_ref=[x_ini,y_ini,field.z]
        self.pos_aim=[x_ini,y_ini,field.z]
        self.pos=[self.team.wing*x_ini,y_ini,field.z]
        
        #now we can load pictures
        self.anim[1]={} #dictionnary of all animation looking to the right
        self.anim[1]["walk"]=[]
        self.anim[1]["walk"].append(compileimage(self.team.body_number,"walk_A.png",self.head_number,"normal.png",(2,0)))
        self.anim[1]["walk"].append(compileimage(self.team.body_number,"walk_B.png",self.head_number,"normal.png",(2,0)))
        self.anim[1]["walk"].append(compileimage(self.team.body_number,"walk_C.png",self.head_number,"normal.png",(2,0)))
        self.anim[1]["walk"].append(compileimage(self.team.body_number,"walk_D.png",self.head_number,"normal.png",(2,0)))
        self.anim[1]["walk"].append(compileimage(self.team.body_number,"walk_E.png",self.head_number,"normal.png",(2,0)))
        self.anim[1]["walk"].append(compileimage(self.team.body_number,"walk_F.png",self.head_number,"normal.png",(2,0)))
        self.anim[1]["walk"].append(compileimage(self.team.body_number,"walk_G.png",self.head_number,"normal.png",(2,0)))
        self.anim[1]["jump"]=[]
        self.anim[1]["jump"].append(compileimage(self.team.body_number,"jump_A.png",self.head_number,"normal.png",(2,0)))
        self.anim[1]["jump"].append(compileimage(self.team.body_number,"jump_A.png",self.head_number,"normal.png",(2,0)))
        self.anim[1]["shoot"]=[]
        self.anim[1]["shoot"].append(compileimage(self.team.body_number,"shoot_A.png",self.head_number,"back.png",(14,0)))
        self.anim[1]["shoot"].append(compileimage(self.team.body_number,"shoot_B.png",self.head_number,"normal.png",(6,1)))
        self.anim[1]["shoot"].append(compileimage(self.team.body_number,"shoot_C.png",self.head_number,"normal.png",(6,0)))
        self.anim[1]["attack"]=[]
        self.anim[1]["attack"].append(compileimage(self.team.body_number,"attack_A.png",self.head_number,"angry.png",(9,1)))
        self.anim[1]["hurt"]=[]
        self.anim[1]["hurt"].append(compileimage(self.team.body_number,"hurt_A.png",self.head_number,"hurt.png",(1,1)))
        
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
            self.anim_index += 0.04
            self.pos[0]-=self.direction/10.0
            if (self.anim_index>=len(self.anim[self.direction][self.state])):
                self.anim_index=0
                self.state="walk"
            
        #try to catch the ball  : see player_GK and player_non_GK

        #update animation
        if (self.anim_index>=len(self.anim[self.direction][self.state])):
            self.anim_index=0
        self.image = self.anim[self.direction][self.state][int(self.anim_index)]
    
        match.field.collide_with_player(self)
        
        self.dist2_to_ball=(self.pos[0]-match.ball.pos[0])**2+(self.pos[1]-match.ball.pos[1])**2 #square of planar dist to ball

    
    def draw(self,surface,camera,is_shadow=True):
        Sprite.draw(self,surface,camera,is_shadow)
        #surface.blit(self.team.image, camera.proj([self.pos[0],self.pos[1],self.pos[2]],self.team.image.get_width(),self.team.image.get_height()*3))
    
    def shoot(self,match):
        if (match.ball.owner==0) or (self.has_ball==0):
            print("Error on shoot!")
            match.ball.owner=0
            self.has_ball=0
            return

        self.state="shoot"
        self.anim_index=0

        match.ball.speed[0]=int(self.inputs.R)*4*self.kick - int(self.inputs.L)*4*self.kick + 8*self.direction*self.kick
        match.ball.speed[1]=int(self.inputs.U)*8*self.kick - int(self.inputs.D)*8*self.kick
        match.ball.speed[2]=8-int(self.inputs.R)*4 - int(self.inputs.L)*4

        match.ball.owner=0
        self.has_ball=0
        Player.snd_shoot.play()


    def pass_ball(self,match):
        if (match.ball.owner==0) or (self.has_ball==0):
            print("Error on shoot!")
            match.ball.owner=0
            self.has_ball=0
            return

        self.state="shoot"
        self.anim_index=0

        best_teammate=0 #closer to the ball in good angle
        best_teammate_az=0
        best_teammate2=0 #closer to the ball in next angle
        best_teammate2_az=0

        if (self.inputs.U or self.inputs.R or self.inputs.D or self.inputs.L):
            #find player in right direction
            #angle 0: north, 1: north-east ... 7: north-west
            if (self.inputs.U):
                aiming_angle=0
            if (self.inputs.D):
                aiming_angle=4
            if (self.inputs.R):
                aiming_angle=2
                if (self.inputs.U):
                    aiming_angle=1
                if (self.inputs.D):
                    aiming_angle=3
            if (self.inputs.L):
                aiming_angle=6
                if (self.inputs.U):
                    aiming_angle=7
                if (self.inputs.D):
                    aiming_angle=5
            #print("aim: "+str(aiming_angle))
            #find whom to pass the ball
            for p in self.team.players_ordered_dist_to_ball:
                if (p!=self):
                    az=math.atan2(p.pos[0]-self.pos[0],p.pos[1]-self.pos[1])
                    az_int=int(((az+math.pi/8)/(math.pi/4))+8) % 8
                    #print(az*180/math.pi,az_int)
                    if ((az_int%8)==aiming_angle):
                        best_teammate=p
                        best_teammate_az=az
                        #print("ok!")
                        break
                    if ((((az_int+1)%8)==aiming_angle) or (((az_int+7)%8)==aiming_angle)):
                        best_teammate2=p
                        best_teammate2_az=az
                        #print("bof.")

            if (best_teammate==0):
                if (best_teammate2!=0):
                    best_teammate=best_teammate2
                    best_teammate_az=best_teammate2_az
                else:
                    return
        else:#no direction enterded, find closest teammate
            if (len(self.team.players_ordered_dist_to_ball)<2):
                return #nobody to bass the ball to
            best_teammate=self.team.players_ordered_dist_to_ball[1]
            best_teammate_az=math.atan2(best_teammate.pos[0]-self.pos[0],best_teammate.pos[1]-self.pos[1])


        #compute pass speed... 
        best_teammate_dist=math.sqrt((best_teammate.pos[0]-self.pos[0])**2+(best_teammate.pos[1]-self.pos[1])**2)
        power=min(best_teammate_dist,8*self.kick)

        best_teammate_az+=(random.random()-0.5)/1.5*self.precision

        match.ball.speed[0]=math.sin(best_teammate_az)*power
        match.ball.speed[1]=math.cos(best_teammate_az)*power
        match.ball.speed[2]=power/2

        match.ball.owner=0
        self.has_ball=0
        Player.snd_pass.play()


    def attack(self,match):
        self.state="attack"
        self.anim_index=0

        for p in match.player_list:
            if (p!=self):
                if (0<(p.pos[0]-self.pos[0])*self.direction<6) \
                    and (abs(p.pos[1]-self.pos[1])<5) \
                    and (abs(p.pos[2]-self.pos[2])<5):
                    #p is attacked !
                    p.state="hurt"
                    Player.snd_attack.play()
                    p.anim_index=0
                    p.direction=-self.direction
                    p.health-=5*self.punch/p.resistance
                    if (p.health<0):
                        p.health=0
                    if (p.has_ball != 0):
                        p.has_ball=0
                        match.ball.owner=0
                        match.ball.speed[0]+=5*self.direction

    def handle_inputs(self,match):
        if (self.state=="walk"):
            if (self.has_ball!=0): #with ball: slower
                if self.inputs.L:
                    self.pos[0] -= self.speed#*0.8
                    self.energy -= 1
                    self.direction = -1
                if self.inputs.R:
                    self.pos[0] += self.speed#*0.8
                    self.energy -= 1
                    self.direction = +1
                if self.inputs.U:
                    self.pos[1] += self.speed#*0.8
                    self.energy -= 1
                if self.inputs.D:
                    self.pos[1] -= self.speed#*0.8
                    self.energy -= 1
            else:#don't have ball
                if self.inputs.L:
                    self.pos[0] -= self.speed
                    self.direction = -1
                if self.inputs.R:
                    self.pos[0] += self.speed
                    self.direction = +1
                if self.inputs.U:
                    self.pos[1] += self.speed
                if self.inputs.D:
                    self.pos[1] -= self.speed
            if (self.inputs.L or self.inputs.R or self.inputs.U or self.inputs.D):
                self.anim_index += 0.3
            # Jump if the player presses the C button
            if (self.inputs.C and self.pos[2] == 0):
                self.jump_speed = 2.5*self.jump_hight
                self.state="jump"
                self.anim_index=0
                
            if (self.inputs.B):
                if (self.has_ball==0):
                    self.attack(match)
            if (self.inputs.B):
                if (self.has_ball!=0):
                    self.shoot(match)
            if (self.inputs.A):
                if (self.has_ball!=0):
                    self.pass_ball(match)
            
        self.inputs.update() #read the new keys or clear inputs for CPU



