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
from player import Player

class Player_non_GK(Player):
    
    def __init__(self, team, head,pos_init,field_half_length):
        Player.__init__(self,team,head,pos_init,field_half_length)
        
    def update(self,match):
        #try to catch the ball 
        if (self.state=="walk") and (match.ball.owner==0):
            if (abs(match.ball.pos[0]-self.pos[0]-self.direction*1)<4) \
                and (abs(match.ball.pos[1]-self.pos[1])<5)  \
                and ((match.ball.pos[2]-self.pos[2])<7): #Z
                if (abs(match.ball.speed[0])>9*self.control):#too much in opposite direction : KO
                    self.state="hurt"
                    self.anim_index=0
                    match.ball.speed[0]*=-0.6
                    match.ball.speed[2]+=(match.ball.pos[2]-self.pos[2])
                    Player.snd_pass.play()
                else:#not enought to hurt...
                    if (match.ball.speed[0]*self.direction<10):#speed X must be slow or in opposite direction
                        match.ball.owner=self
                        self.has_ball=match.ball
                        match.ball.speed=[0,0,0]
        Player.update(self,match)

