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
import fnmatch
from math import cos
from inputs import Inputs

from team import Team

from retrogamelib import display
from retrogamelib import font
from retrogamelib.constants import *

from retrogamelib import dialog

#Global variables, to have options saved during all session
#see menus declaration to understand what those options mean
default_options=[]
default_options.append(1)
default_options.append(0)
default_options.append(1)
default_options.append(1)
default_options.append(0)#west team index
default_options.append(1)#east team index


def show_info(display,font,mainClock):
    title_image=pygame.image.load("data/title.png")

    dialogbox = dialog.DialogBox((240, 51), (0, 0, 0),(255, 255, 255), font)
    dialogbox.set_dialog([
        "Welcome to pyNekketsu!      Press L to continue.", 
        "Player1 controls:           arrows (to move),           K (shoot or attack),        L (pass), P (pause, start)", 
        "Player2 controls:           F, G, H, T (to move),       A (shoot or attack),        Z (pass), R (pause, start)"])

    while not dialogbox.over():
        mainClock.tick(30)
        
        Inputs.readkeys()#read all the actual keys
          
        if (Inputs.player_just_Esc[1] or Inputs.player_just_Esc[2]):
            pygame.quit()
            sys.exit()

        if Inputs.player_just_A[1]:
            dialogbox.progress()
        
        # Get the surface from the NES game library
        screen = display.get_surface()
        screen.blit(title_image,(0,0))
        
        dialogbox.draw(screen, (8, 128))

        # Update and draw the display
        display.update()
 


def call_a_menu(menu,default_option,info,display,font,mainClock):
    menu.option=default_option
    title_image=pygame.image.load("data/title.png")
    while 1:
        mainClock.tick(30)
        Inputs.readkeys()#read all the actual keys
        if (Inputs.player_just_Esc[1] or Inputs.player_just_Esc[2]):
            pygame.quit()
            sys.exit()
        # Move the menu cursor if you press up or down    
        if Inputs.player_just_U[1]:
            menu.move_cursor(-1)
        if Inputs.player_just_D[1]:
            menu.move_cursor(1)
        # If you press A, check which option you're on!
        if Inputs.player_just_A[1]:
            option, text = menu.get_option()
            return option, text
        # If you press B, cancel 
        if Inputs.player_just_B[1]:
            return -1, ""
        
        # Get the surface from the NES game library
        screen = display.get_surface()
        screen.blit(title_image,(0,0))
        
        # Draw the menu boxes
        ren = font.render(info)
        screen.blit(ren, (8, 112))
        menu.draw(screen, (16, 128), background=(0, 0, 0), border=(255, 255, 255))
        # Update and draw the display
        display.update()


def call_all_menus(display,font,mainClock):
    players_human_teamA=0
    players_human_teamB=0
    difficulty=0
    nb_player_team=0
    match_length=0
    teamA_filename=0
    teamB_filename=0
    
    menu_players = dialog.Menu(font, ["No human player", "Player1 VS CPU","Player1 VS Player2","Player1 + Player2 VS CPU"])
    menu_diff = dialog.Menu(font, ["too easy", "easy","medium", "hard", "too hard"])
    menu_nb_play_team = dialog.Menu(font, ["1", "2", "3", "4"])
    menu_match_length = dialog.Menu(font, ["30", "60","120", "300", "450"])
    #next menu is select_teams
    west_team_index=0
    east_team_index=1#default teams

    menus=[]
    menus.append(menu_players)
    menus.append(menu_diff)
    menus.append(menu_nb_play_team)
    menus.append(menu_match_length)
    info=[]
    info.append("Select game mode:")
    info.append("Select game difficulty:")
    info.append("Number of players per team:")
    info.append("Match length in seconds:")

    current_menu=0 #index in "menus"

    while current_menu<len(menus)+1:
        if (current_menu<len(menus)):
            option, text=call_a_menu(menus[current_menu],default_options[current_menu],info[current_menu],display,font,mainClock)
            if (option==-1) and (current_menu>0):
                current_menu-=1
            else:
                default_options[current_menu]=option #save for later...
                if (current_menu==0):#about game mode
                    if (option==0):
                        players_human_teamA=0
                        players_human_teamB=0
                    if (option==1):
                        players_human_teamA=1
                        players_human_teamB=0
                    if (option==2):
                        players_human_teamA=1
                        players_human_teamB=1
                    if (option==3):
                        players_human_teamA=2
                        players_human_teamB=0
                elif (current_menu==1): #about difficulty
                    difficulty=2+option*2 
                elif (current_menu==2): #about nbr players
                    nb_player_team=int(text)
                elif (current_menu==3): #about match length
                    match_length=int(text)

                current_menu+=1
        else:#final menu: select_teams
            west_team_index=default_options[current_menu]
            east_team_index=default_options[current_menu+1]
            (teamA_filename,west_team_index,teamB_filename,east_team_index)=select_teams(display,font,mainClock,west_team_index,east_team_index)
            if ((teamA_filename=="?") or (teamA_filename=="?")) and (current_menu>0):
                current_menu-=1
            else:
                default_options[current_menu]=west_team_index#save for later...
                default_options[current_menu+1]=east_team_index#save for later...
                current_menu+=1

    return players_human_teamA,players_human_teamB,difficulty,nb_player_team,match_length,teamA_filename,teamB_filename

    
def draw_team_info_text(screen,font,x):
    y=160
    x_scale=1
    y_gap=10
    color=(200,200,0)
    ren = font.render("speed")
    screen.blit(ren,(x+font.center_shift("speed"),y-4))
    y+=y_gap
    ren = font.render("resistance")
    screen.blit(ren,(x+font.center_shift("resistance"),y-4))
    y+=y_gap
    ren = font.render("control")
    screen.blit(ren,(x+font.center_shift("control"),y-4))
    y+=y_gap
    ren = font.render("kick")
    screen.blit(ren,(x+font.center_shift("kick"),y-4))
    y+=y_gap
    ren = font.render("punch")
    screen.blit(ren,(x+font.center_shift("punch"),y-4))
    y+=y_gap
    ren = font.render("precision")
    screen.blit(ren,(x+font.center_shift("precision"),y-4))
    y+=y_gap
    ren = font.render("listening")
    screen.blit(ren,(x+font.center_shift("listening"),y-4))
    y+=y_gap
    
 
def select_teams(display,font,mainClock,west_team_index_init,east_team_index_init):
    path="data/teams/"
    dirList=os.listdir(path)
    allteams=[]
    for fname in dirList:
        if fnmatch.fnmatch(fname, '*.xml'):
            allteams.append(Team("data/teams/"+fname))
    
    title_image=pygame.image.load("data/title.png")

    cursor_on_east_wing=False
    cursor_color_angle=0
    west_team_index=west_team_index_init
    east_team_index=east_team_index_init
    while 1:
        mainClock.tick(30)
        cursor_color_angle+=0.1
        Inputs.readkeys()#read all the actual keys
        if (Inputs.player_just_Esc[1] or Inputs.player_just_Esc[2]):
            pygame.quit()
            sys.exit()
        # Move the menu cursor if you press up or down    
        if Inputs.player_just_U[1]:
            if (cursor_on_east_wing):
                east_team_index-=1
                if (east_team_index<0):
                    east_team_index=len(allteams)-1
                if (east_team_index==west_team_index):
                    east_team_index-=1
                    if (east_team_index<0):
                        east_team_index=len(allteams)-1
            else:
                west_team_index-=1
                if (west_team_index<0):
                    west_team_index=len(allteams)-1
                if (east_team_index==west_team_index):
                    west_team_index-=1
                    if (west_team_index<0):
                        west_team_index=len(allteams)-1
        if Inputs.player_just_D[1]:
            if (cursor_on_east_wing):
                east_team_index+=1
                if (east_team_index>=len(allteams)):
                    east_team_index=0
                if (east_team_index==west_team_index):
                    east_team_index+=1
                    if (east_team_index>=len(allteams)):
                        east_team_index=0
            else:
                west_team_index+=1
                if (west_team_index>=len(allteams)):
                    west_team_index=0
                if (east_team_index==west_team_index):
                    west_team_index+=1
                    if (west_team_index>=len(allteams)):
                        west_team_index=0
        if Inputs.player_just_R[1] or Inputs.player_just_L[1]:
                cursor_on_east_wing=not cursor_on_east_wing
        # If you press A, check which option you're on!
        if Inputs.player_just_A[1]:
            return (allteams[west_team_index].xml_filename,west_team_index,allteams[east_team_index].xml_filename,east_team_index)
        # If you press B, cancel 
        if (Inputs.player_just_B[1]):# or  Inputs.player_just_Esc[1] or Inputs.player_just_Esc[2]):
            return ("?",west_team_index,"?",east_team_index)
        
        
        # Get the surface from the NES game library
        screen = display.get_surface()
        screen.blit(title_image,(0,0))
        
        #draw current teams
        if (cursor_on_east_wing):
            pygame.draw.rect(screen, (150+cos(cursor_color_angle)*50,150+cos(cursor_color_angle+2.1)*50 ,150+cos(cursor_color_angle+1.2)*50 ), (185, 115, 25,25),1)
        else:
            pygame.draw.rect(screen, (150+cos(cursor_color_angle)*50,150+cos(cursor_color_angle+2.1)*50 ,150+cos(cursor_color_angle+1.2)*50), (37, 115, 25,25),1)

        draw_team_info_text(screen,font,128)
        #screen.blit(allteams[west_team_index].image,(42,120))
        transf_west_img=pygame.transform.scale(allteams[west_team_index].image,(int(16+4*cos(cursor_color_angle)),int(16+4*cos(1.3*cursor_color_angle+0.5))))
        transf_west_img=pygame.transform.scale(allteams[west_team_index].image,(int(16+4*cos(cursor_color_angle)),int(16+4*cos(1.3*cursor_color_angle+0.5))))
        transf_east_img=pygame.transform.scale(allteams[east_team_index].image,(int(16+4*cos(cursor_color_angle+1)),int(16+4*cos(1.3*cursor_color_angle+1.5))))

        screen.blit(transf_west_img,(42+8-(16+4*cos(cursor_color_angle))/2,120+8-(16+4*cos(1.3*cursor_color_angle+0.5))/2))
        screen.blit(transf_east_img,(192+8-(16+4*cos(cursor_color_angle+1))/2,120+8-(16+4*cos(1.3*cursor_color_angle+1.5))/2))

        allteams[west_team_index].draw_info(screen,78,-1)
        allteams[east_team_index].draw_info(screen,178,1)
        
        ren = font.render(allteams[west_team_index].name)
        screen.blit(ren, (55+font.center_shift(allteams[west_team_index].name), 142))
        ren = font.render(allteams[east_team_index].name)
        screen.blit(ren, (200+font.center_shift(allteams[east_team_index].name), 142))
        ren = font.render("vs.")
        screen.blit(ren, (120, 125))


#        x=100
#        y=100
#        draw_team_info_text(screen,font,10)
#        for team in allteams:
#            screen.blit(team.image,(x,y))
#            team.draw_info(screen,x)
#            x+=50
        # Draw the menu boxes
        #ren = font.render(info)
        #screen.blit(ren, (8, 112))
        # Update and draw the display
        display.update()

