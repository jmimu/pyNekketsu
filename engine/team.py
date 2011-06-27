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
from player_cpu import Player_CPU
from player_GK import Player_GK
from inputs import Inputs
import random


#number of differents heads 
nbr_heads=3


#
class Team(object):
    def __init__(self, number, img_team, name_team, wing, field, nb_players_cpu):#wing where they look: -1 (west) or +1 (east)
        self.number=number
        self.image=pygame.image.load(img_team)
        self.name=name_team
        self.nb_goals=0
        self.wing=wing #wing for target, -wing for own goal
        self.players=[] #first is GK, last are human players
        self.players_ordered_dist_to_ball=[]
        #add the GK
        self.players.append(Player_GK(self,random.randint(1, nbr_heads), [-self.wing*field.half_length, field.goal_latitude[-self.wing],0 ],field.half_length))
        #add the other players
        for i in range(nb_players_cpu):
            self.players.append(Player_CPU(self,random.randint(1, nbr_heads),[-self.wing*field.half_length*((i+1.0)/(nb_players_cpu+1.0)), random.randint(-field.half_width,field.half_width),0],field.half_length))
    
        self.players_ordered_dist_to_ball[:]=self.players[1:]
    
    def update(self,match):
        #if has to pass to player 1
        if (match.player1!=0) and (match.player1.team==self) and (Inputs.player1_just_A) and (match.ball.owner!=0) and (match.ball.owner.number_human_player==0) and (match.ball.owner.team==self):
            if (random.random()<0.35*match.ball.owner.listening):
                #aim to the player ?
                match.ball.owner.inputs.A=True
                match.ball.owner.inputs.U=False
                match.ball.owner.inputs.D=False
                match.ball.owner.inputs.L=False
                match.ball.owner.inputs.R=False
        if (match.player2!=0) and (match.player2.team==self) and (Inputs.player2_just_A) and (match.ball.owner!=0) and (match.ball.owner.number_human_player==0) and (match.ball.owner.team==self):
            if (random.random()<0.35*match.ball.owner.listening):
                #aim to the player ?
                match.ball.owner.inputs.A=True
                match.ball.owner.inputs.U=False
                match.ball.owner.inputs.D=False
                match.ball.owner.inputs.L=False
                match.ball.owner.inputs.R=False



        for p in self.players:
            p.update(match)

        self.players_ordered_dist_to_ball=sorted( self.players_ordered_dist_to_ball,   key=lambda Player: Player.dist2_to_ball) #sort all the perses list with dist2_to_ball

