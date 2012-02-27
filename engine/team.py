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
from sprite import coloringimage
from settings import configuration

class Team(object):
    def __init__(self,xml_file):#wing where they look: -1 (west) or +1 (east)
        self.outfit_img=0
        self.image=0
        self.name="?"
        self.top_color=()
        self.bottom_color=()
        self.nb_goals=0
        self.wing=1 #-wing for target, +wing for own goal
        self.players=[] #first is GK, last are human players
        self.players_ordered_dist_to_ball=[]
        self.team_node = 0 #in xml file (test if 0 to know if beginning of file already read)
        self.xml_filename="?" #to be able to re-read the file if team is selected

        #average to help choosing teams
        self.avg_speed=0
        self.avg_health=0
        self.avg_max_energy=0 #before speed decreases
        self.avg_resistance=0 #before going KO
        self.avg_control=0 #before being hurt by ball
        self.avg_kick=0 #for shooting
        self.avg_punch=0 #for attacking
        self.avg_jump_hight=0 
        self.agressivity=1 
        self.precision=1 #for GK and pass
        self.listening=1 #when asked for pass (max:2)
 
        #those 3 dictionaries will be used to compile each players' sprite
        self.ref_anim_body_img={}#body images dictionary for each status, reference for players' animation
        self.ref_anim_head_name={}#head name dictionary
        self.ref_anim_head_shift={}#head shift dictionary
        #a dict used for animation speed
        self.ref_anim_speed={}
        
        self.read_xml(xml_file)#begin to read xml (general info for team)


    #read some info from xml (minimum to be able to choose your team)
    def read_xml(self, xml_file):
        self.xml_filename=xml_file
        xmldoc = minidom.parse(xml_file)
        self.team_node = xmldoc.getElementsByTagName('team')[0]
        self.image=pygame.image.load(self.team_node.getElementsByTagName('img')[0].childNodes[0].data)
        self.name=self.team_node.getElementsByTagName('name')[0].childNodes[0].data
        #colors:
        r=g=b=128
        r=int(self.team_node.getElementsByTagName('top_color')[0].getElementsByTagName('r')[0].childNodes[0].data)
        g=int(self.team_node.getElementsByTagName('top_color')[0].getElementsByTagName('g')[0].childNodes[0].data)
        b=int(self.team_node.getElementsByTagName('top_color')[0].getElementsByTagName('b')[0].childNodes[0].data)
        self.top_color=(r,g,b)
        r=int(self.team_node.getElementsByTagName('bottom_color')[0].getElementsByTagName('r')[0].childNodes[0].data)
        g=int(self.team_node.getElementsByTagName('bottom_color')[0].getElementsByTagName('g')[0].childNodes[0].data)
        b=int(self.team_node.getElementsByTagName('bottom_color')[0].getElementsByTagName('b')[0].childNodes[0].data)
        self.bottom_color=(r,g,b)
 
        self.outfit_img=(coloringimage("outfit.png",self.top_color,self.bottom_color))
        
        #get avg caract.
        self.avg_speed=0
        self.avg_health=0
        self.avg_max_energy=0 #before speed decreases
        self.avg_resistance=0 #before going KO
        self.avg_control=0 #before being hurt by ball
        self.avg_kick=0 #for shooting
        self.avg_punch=0 #for attacking
        self.avg_jump_hight=0 
        self.avg_agressivity=0 
        self.avg_precision=0 #for GK and pass
        self.avg_listening=0

        players_node = self.team_node.getElementsByTagName('players')[0]
        all_players=players_node.getElementsByTagName('player')
        all_players.append(players_node.getElementsByTagName('playerGK')[0])
        nbr_players=0
        for player_node in all_players:
            self.avg_speed+=float(player_node.getElementsByTagName('speed')[0].childNodes[0].data)
            self.avg_health+=float(player_node.getElementsByTagName('health')[0].childNodes[0].data)
            self.avg_max_energy+=float(player_node.getElementsByTagName('max_energy')[0].childNodes[0].data)
            self.avg_resistance+=float(player_node.getElementsByTagName('resistance')[0].childNodes[0].data)
            self.avg_control+=float(player_node.getElementsByTagName('control')[0].childNodes[0].data)
            self.avg_kick+=float(player_node.getElementsByTagName('kick')[0].childNodes[0].data)
            self.avg_punch+=float(player_node.getElementsByTagName('punch')[0].childNodes[0].data)
            self.avg_jump_hight+=float(player_node.getElementsByTagName('jump_hight')[0].childNodes[0].data) 
            self.avg_agressivity+=float(player_node.getElementsByTagName('agressivity')[0].childNodes[0].data)
            self.avg_precision+=float(player_node.getElementsByTagName('precision')[0].childNodes[0].data)
            self.avg_listening+=float(player_node.getElementsByTagName('listening')[0].childNodes[0].data)
            nbr_players+=1

        self.avg_speed/=nbr_players
        self.avg_health/=nbr_players
        self.avg_max_energy/=nbr_players
        self.avg_resistance/=nbr_players
        self.avg_control/=nbr_players
        self.avg_kick/=nbr_players
        self.avg_punch/=nbr_players
        self.avg_jump_hight/=nbr_players
        self.avg_agressivity/=nbr_players
        self.avg_precision/=nbr_players
        self.avg_listening/=nbr_players

        return self.team_node
                                                                       
    #part of creation of the team when wing are decided
    #create players and read xml
    #human_players: array of human players id
    def create_from_xml(self,wing,nb_players_total,human_players,match):
        self.wing=wing #-wing for target, +wing for own goal
        if (self.team_node==0):
            self.team_node=self.read_xml(self.xml_filename)

        #read all the animations
        xmldoc = minidom.parse("data/player_animations.xml")
        animations_node = xmldoc.getElementsByTagName('animations')[0]
        all_anims=animations_node.getElementsByTagName('anim')
        for anim_node in all_anims:
            anim_name=anim_node.getElementsByTagName('name')[0].childNodes[0].data
            anim_speed=float(anim_node.getElementsByTagName('speed')[0].childNodes[0].data)
            self.ref_anim_body_img[anim_name]=[]
            self.ref_anim_head_name[anim_name]=[]
            self.ref_anim_head_shift[anim_name]=[]
            self.ref_anim_speed[anim_name]=anim_speed
            all_imgs=anim_node.getElementsByTagName('img')
            for img_node in all_imgs:
                img_filename=img_node.getElementsByTagName('img_name')[0].childNodes[0].data
                img_headfilename=img_node.getElementsByTagName('head_img')[0].childNodes[0].data
                img_head_x=int(img_node.getElementsByTagName('head_x')[0].childNodes[0].data)
                img_head_y=int(img_node.getElementsByTagName('head_y')[0].childNodes[0].data)
                self.ref_anim_body_img[anim_name].append(coloringimage(img_filename,self.top_color,self.bottom_color))
                self.ref_anim_head_name[anim_name].append(img_headfilename)
                self.ref_anim_head_shift[anim_name].append((img_head_x,img_head_y))

 
        players_node = self.team_node.getElementsByTagName('players')[0]
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
            #adjust speed to change difficulty (8:hard = normal speed)
            self.players[-1].speed/=(1.0+(8-Player_CPU.difficulty)/10.0)

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



    def draw_info(self,surface,x,direction=1):
        y=160
        x_scale=direction
        y_gap=10
        color=(200,200,0)

        normal_speed=1
        x_speed=((self.avg_speed-normal_speed)*100+20)*x_scale
        x_normal_speed=20*x_scale
        #pygame.draw.line(surface, (150,150,150),(x,y),(x+x_normal_speed,y),7)
        pygame.draw.line(surface, color,(x,y),(x+x_speed,y),3)
        y+=y_gap
        
        normal_resistance=1
        x_resistance=((self.avg_resistance-normal_resistance)*100+20)*x_scale
        x_normal_resistance=20*x_scale
        #pygame.draw.line(surface, (150,150,150),(x,y),(x+x_normal_resistance,y),7)
        pygame.draw.line(surface, color,(x,y),(x+x_resistance,y),3)
        y+=y_gap
        
        normal_control=1
        x_control=((self.avg_control-normal_control)*100+20)*x_scale
        x_normal_control=20*x_scale
        #pygame.draw.line(surface, (150,150,150),(x,y),(x+x_normal_control,y),7)
        pygame.draw.line(surface, color,(x,y),(x+x_control,y),3)
        y+=y_gap
        
        normal_kick=1
        x_kick=((self.avg_kick-normal_kick)*100+20)*x_scale
        x_normal_kick=20*x_scale
        #pygame.draw.line(surface, (150,150,150),(x,y),(x+x_normal_kick,y),7)
        pygame.draw.line(surface, color,(x,y),(x+x_kick,y),3)
        y+=y_gap
        
        normal_punch=1
        x_punch=((self.avg_punch-normal_punch)*100+20)*x_scale
        x_normal_punch=20*x_scale
        #pygame.draw.line(surface, (150,150,150),(x,y),(x+x_normal_punch,y),7)
        pygame.draw.line(surface, color,(x,y),(x+x_punch,y),3)
        y+=y_gap
        
        normal_precision=1
        x_precision=((self.avg_precision-normal_precision)*100+20)*x_scale
        x_normal_precision=20*x_scale
        #pygame.draw.line(surface, (150,150,150),(x,y),(x+x_normal_precision,y),7)
        pygame.draw.line(surface, color,(x,y),(x+x_precision,y),3)
        y+=y_gap
 
        normal_listening=1
        x_listening=((self.avg_listening-normal_listening)*100+20)*x_scale
        x_normal_listening=20*x_scale
        #pygame.draw.line(surface, (150,150,150),(x,y),(x+x_normal_listening,y),7)
        pygame.draw.line(surface, color,(x,y),(x+x_listening,y),3)
        y+=y_gap
        
       
