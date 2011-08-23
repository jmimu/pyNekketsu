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
from xml.dom import minidom

from player_cpu import Player_CPU
from player_GK import Player_GK
from player_human import Player_Human
from inputs import Inputs


#number of differents heads 
nbr_heads=4


#
class Team(object):
    def __init__(self, wing, field ):#wing where they look: -1 (west) or +1 (east)
        self.body_number=0
        self.image=0
        self.name="?"
        self.top_color=()
        self.bottom_color=()
        self.nb_goals=0
        self.wing=wing #-wing for target, +wing for own goal
        self.players=[] #first is GK, last are human players
        self.players_ordered_dist_to_ball=[]

        self.ref_anim={}#dictionnary for right and left, reference for players' animation
        #read all the animations
        xmldoc = minidom.parse("data/animations.xml")
        animations_node = xmldoc.getElementsByTagName('animations')[0]
        all_anims=animations_node.getElementsByTagName('anim')
        for anim_node in all_anims:
            anim_name=anim_node.getElementsByTagName('name')[0].childNodes[0].data
            anim_speed=anim_node.getElementsByTagName('speed')[0].childNodes[0].data
            #TODO: insert pic in ref_anim !
            all_imgs=anim_node.getElementsByTagName('img')
            for img_node in all_imgs:
                img_filename=img_node.getElementsByTagName('img_name')[0].childNodes[0].data
                img_headfilename=img_node.getElementsByTagName('head_img')[0].childNodes[0].data
                img_head_x=int(img_node.getElementsByTagName('head_x')[0].childNodes[0].data)
                img_head_y=int(img_node.getElementsByTagName('head_y')[0].childNodes[0].data)


    
    #read some info from xml (minimum to be able to choose your team)
    def read_xml(self, xml_file):
        xmldoc = minidom.parse(xml_file)
        team_node = xmldoc.getElementsByTagName('team')[0]
        self.body_number=team_node.getElementsByTagName('body_number')[0].childNodes[0].data
        self.image=pygame.image.load(team_node.getElementsByTagName('img')[0].childNodes[0].data)
        self.name=team_node.getElementsByTagName('name')[0].childNodes[0].data
        #colors:
        r=g=b=128
        r=int(team_node.getElementsByTagName('top_color')[0].getElementsByTagName('r')[0].childNodes[0].data)
        g=int(team_node.getElementsByTagName('top_color')[0].getElementsByTagName('g')[0].childNodes[0].data)
        b=int(team_node.getElementsByTagName('top_color')[0].getElementsByTagName('b')[0].childNodes[0].data)
        self.top_color=(r,g,b)
        r=int(team_node.getElementsByTagName('bottom_color')[0].getElementsByTagName('r')[0].childNodes[0].data)
        g=int(team_node.getElementsByTagName('bottom_color')[0].getElementsByTagName('g')[0].childNodes[0].data)
        b=int(team_node.getElementsByTagName('bottom_color')[0].getElementsByTagName('b')[0].childNodes[0].data)
        self.bottom_color=(r,g,b)
        return team_node
                                                                       
    #create players and read xml
    def create_from_xml(self,xml_file,nb_players_total,human_players,match):#human_players: array of human players id
        team_node=self.read_xml(xml_file)

        players_node = team_node.getElementsByTagName('players')[0]
        GK_node = players_node.getElementsByTagName('playerGK')[0]
        
        #add the GK
        self.players.append(Player_GK(self))
        self.players[0].read_xml(GK_node,match.field)
        
        player_rank=0
        
        #add human players
        for id_human in human_players:
            match.human_players[id_human] = Player_Human(self,id_human,"data/"+str(id_human)+".png")
            self.players.append(match.human_players[id_human])#add the player to the team
            self.players_ordered_dist_to_ball.append(match.human_players[id_human])#add the player to closest to ball order
            player_node=players_node.getElementsByTagName('player')[player_rank]
            player_rank=player_rank+1
            self.players[-1].read_xml(player_node,match.field)

        #add the other players
        for i in range(nb_players_total-len(human_players)):
            self.players.append(Player_CPU(self))
            player_node=players_node.getElementsByTagName('player')[player_rank]
            player_rank=player_rank+1
            self.players[-1].read_xml(player_node,match.field)

        self.players_ordered_dist_to_ball[:]=self.players[1:]

    
    def update(self,match):
        for i in range(1,3):
            #if has to pass to human player
            if (match.human_players[i]!=0) and (match.human_players[i].team==self) and (Inputs.player_just_A[i]) and (match.ball.owner!=0) and (match.ball.owner.number_human_player==0) and (match.ball.owner.team==self):
                if (random.random()<0.35*match.ball.owner.listening):
                    #aim to the player ?
                    match.ball.owner.inputs.A=True
                    match.ball.owner.inputs.U=False
                    match.ball.owner.inputs.D=False
                    match.ball.owner.inputs.L=False
                    match.ball.owner.inputs.R=False

            #if AI player is asked to shoot
            if (match.human_players[i]!=0) and (match.human_players[i].team==self) and (Inputs.player_just_B[i]) and (match.ball.owner!=0) and (match.ball.owner.number_human_player==0) and (match.ball.owner.team==self):
                if (random.random()<0.35*match.ball.owner.listening):
                    #shoot in the direction P1 is aiming at
                    match.ball.owner.inputs.B=True
                    match.ball.owner.inputs.U=Inputs.player_U[i]
                    match.ball.owner.inputs.D=Inputs.player_D[i]
                    match.ball.owner.inputs.L=Inputs.player_L[i]
                    match.ball.owner.inputs.R=Inputs.player_R[i]


        for p in self.players:
            p.update(match)

        self.players_ordered_dist_to_ball=sorted( self.players_ordered_dist_to_ball,   key=lambda Player: Player.dist2_to_ball) #sort all the perses list with dist2_to_ball

