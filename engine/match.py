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
from player import Player
from player_cpu import Player_CPU
from player_human import Player_Human
from player_GK import Player_GK
from inputs import Inputs
from camera import Camera
from field import Field
from ball import Ball
from sprite import Sprite
from team import Team, nbr_heads
import random

class Match(object):
    snd_whistle = pygame.mixer.Sound("data/sound/etw/fischiolungo.wav")
    
    def __init__(self,nbr_players_human_teamA,nbr_players_teamA,nbr_players_human_teamB,nbr_players_teamB,difficulty=8,length=60):
        Player_CPU.difficulty=difficulty
        Player_GK.difficulty=difficulty

        self.goal_image=pygame.image.load("data/goal.png")
        self.clock_image=pygame.image.load("data/clock.png")
        self.goaldrawing_time=0
        self.is_finished=False
        
        self.match_time=length
        self.human_players=[0,0] #max two players
        self.pause=False
        self.cam=Camera()
        self.field=Field()
        self.ball=Ball()
        self.player_list=[]
        self.team={}#
        
        human_players_teamA=[]
        human_players_teamB=[]
        if (nbr_players_human_teamA>0):
            human_players_teamA.append( 1+len(human_players_teamA)+len(human_players_teamB) )
        if (nbr_players_human_teamA>1):
            human_players_teamA.append( 1+len(human_players_teamA)+len(human_players_teamB) )
        if (nbr_players_human_teamB>0):
            human_players_teamA.append( 1+len(human_players_teamA)+len(human_players_teamB) )
        if (nbr_players_human_teamB>1):
            human_players_teamA.append( 1+len(human_players_teamA)+len(human_players_teamB) )

        self.team[-1]=Team(-1,self.field)
        self.team[-1].read_xml("data/teams/teamA.xml",nbr_players_teamA,human_players_teamA,self)
        self.player_list+=self.team[-1].players
        
        self.team[1]=Team(1,self.field)
        self.team[1].read_xml("data/teams/teamB.xml",nbr_players_teamB,human_players_teamB,self)
        self.player_list+=self.team[1].players
        
        Match.snd_whistle.play()
        
    
    def update(self):
        Inputs.readkeys()#read all the actual keys
        if (Inputs.player1_just_Start or Inputs.player2_just_Start):
            self.pause=not self.pause
            if (self.match_time<=0):
                self.is_finished=True
            else:
                Match.snd_whistle.play()
        
        if (not self.pause):
            #write "Goal!" after a... goal
            if (self.goaldrawing_time<10):
                if (self.goaldrawing_time>0):
                    self.goaldrawing_time-=1

                if (self.match_time>0):#when time is out, players stop
                    self.match_time-=1.0/30 #30 FPS
                    self.team[-1].update(self)
                    self.team[1].update(self)
                if (-1<self.match_time<0):
                    Match.snd_whistle.play()

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

        sprite_list=sorted( [self.ball]+self.player_list,   key=lambda Sprite: -Sprite.pos[1]) #sort all the sprites list with y pos
        for s in sprite_list:
            s.draw(surface,self.cam)
        
        if (self.goaldrawing_time!=0):
            surface.blit(self.goal_image, [0,0])
    

        if (self.pause):
            ren = font.render(" --- PAUSE --- ")
            surface.blit(ren, (8, 16))

        if (self.match_time<=0):
            self.match_time=-1
            ren = font.render("Score: "+str(self.team[-1].nb_goals)+" - "+str(self.team[1].nb_goals))
            surface.blit(ren, (8, 8))
            winner_name=self.team[-1].name
            if (self.team[-1].nb_goals<self.team[1].nb_goals):
                winner_name=self.team[1].name
            if (self.team[-1].nb_goals!=self.team[1].nb_goals):
                ren = font.render(winner_name+" won!")
            else:
                ren = font.render("Draw")
            surface.blit(ren, (32, 32))
            
            ren = font.render("Press Start (P or R)")
            surface.blit(ren, (32, 48))

            ren = font.render("to continue...")
            surface.blit(ren, (64, 56))
        else:
            #had to force number of digits for time and nb goals
            ren = font.render("                 "+str(self.team[-1].nb_goals)+" - "+str(self.team[1].nb_goals)+"     "+str(int(self.match_time)))
            surface.blit(ren, (8, 8))
            surface.blit(self.team[-1].image, (120,2))
            surface.blit(self.team[1].image, (188,2))
            surface.blit(self.clock_image, (240,2))
            
            surface.blit(self.ball.image, (2,4))
            if (self.ball.owner != 0):
                surface.blit(self.team[self.ball.owner.team.wing].image, (20,2))
                ren = font.render(self.ball.owner.name)
                surface.blit(ren, (36, 8))
            
            
