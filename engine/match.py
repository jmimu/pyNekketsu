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

import sys
from perso import Perso
from perso_cpu import PersoCPU
from perso_player import PersoPlayer
from perso_GK import Perso_GK
from inputs import Inputs
from camera import Camera
from field import Field
from ball import Ball
from sprite import Sprite
from team import Team


class Match(object):
    def __init__(self,nbr_players_teamA,nbr_persos_teamA,nbr_players_teamB,nbr_persos_teamB,difficulty=8,length=60):
        PersoCPU.difficulty=difficulty
        Perso_GK.difficulty=difficulty

        self.goal_image=pygame.image.load("data/goal.png")
        self.goaldrawing_time=0
        self.is_finished=False
        
        self.match_time=length
        self.pause=False
        self.cam=Camera()
        self.field=Field()
        self.ball=Ball()
        self.perso_list=[]
        self.teamA=Team(1,"data/teamA.png","Les Bogoss",1,nbr_persos_teamA-nbr_players_teamA)
        if (nbr_players_teamA>0):
            self.player1 = PersoPlayer(self.teamA,3,1,"data/1.png") # Create player1
            self.teamA.persos.append(self.player1)
        if (nbr_players_teamA>1):
            self.player2 = PersoPlayer(self.teamA,2,2,"data/2.png") # Create player2
            self.teamA.persos.append(self.player2)

        self.perso_list+=self.teamA.persos
        self.teamB=Team(2,"data/teamB.png","Les Klass",-1,nbr_persos_teamB-nbr_players_teamB)
        if (nbr_players_teamA>0):
            if (nbr_players_teamB>0):
                self.player2 = PersoPlayer(self.teamB,2,2,"data/2.png") # Create player2
                self.teamB.persos.append(self.player2)
        else:
            if (nbr_players_teamB>0):
                self.player1 = PersoPlayer(self.teamB,1,1,"data/1.png") # Create player1
                self.teamB.persos.append(self.player2)
            if (nbr_players_teamB>1):
                self.player2 = PersoPlayer(self.teamB,2,"data/2.png") # Create player2
                self.teamB.persos.append(self.player2)
 
        self.perso_list+=self.teamB.persos
        
    
    def update(self):
        Inputs.readkeys()#read all the actual keys
        if (Inputs.player1_just_Start or Inputs.player2_just_Start):
            self.pause=not self.pause
            if (self.match_time<=0):
                self.is_finished=True
        
        if (not self.pause):
            #write "Goal!" after a... goal
            if (self.goaldrawing_time<10):
                if (self.goaldrawing_time>0):
                    self.goaldrawing_time-=1

                if (self.match_time>0):#when time is out, players stop
                    self.match_time-=1.0/30 #30 FPS
                    for p in self.perso_list:
                        p.update(self)

                self.ball.update(self)
                
                if (self.ball.owner==0):
                    self.cam.aim_to([self.ball.pos[0],self.ball.pos[1],self.ball.pos[2]/2],0,50)
                else:
                    self.cam.aim_to([self.ball.pos[0],self.ball.pos[1],self.ball.pos[2]/2],self.ball.owner.direction,5)

            else:
                self.goaldrawing_time-=1

        else:#during pause the ball continues to roll
            self.ball.animation()
        


    def draw(self,surface,font):
        self.field.draw(surface,self.cam)

        sprite_list=sorted( [self.ball]+self.perso_list,   key=lambda Sprite: -Sprite.pos[1]) #sort all the sprites list with y pos
        for s in sprite_list:
            s.draw(surface,self.cam)
        
        if (self.goaldrawing_time!=0):
            surface.blit(self.goal_image, [0,0])
    
        ren = font.render("Score: "+str(self.teamA.nb_goals)+" - "+str(self.teamB.nb_goals)+"       TIME: "+str(int(self.match_time)))
        surface.blit(ren, (8, 8))

        if (self.pause):
            ren = font.render(" --- PAUSE --- ")
            surface.blit(ren, (8, 16))

        if (self.match_time<=0):
            winner_name=self.teamA.name
            if (self.teamA.nb_goals<self.teamB.nb_goals):
                winner_name=self.teamB.name
            if (self.teamA.nb_goals!=self.teamB.nb_goals):
                ren = font.render(winner_name+" won!")
            else:
                ren = font.render("Draw")
            surface.blit(ren, (32, 32))
            
            ren = font.render("Press Start (P or R)")
            surface.blit(ren, (32, 48))

            ren = font.render("to continue...")
            surface.blit(ren, (64, 56))
