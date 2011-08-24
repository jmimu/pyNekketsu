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
from inputs import Inputs

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


def show_info(display,font,mainClock):
    title_image=pygame.image.load("data/title.png")

    dialogbox = dialog.DialogBox((240, 51), (0, 0, 0),(255, 255, 255), font)
    dialogbox.set_dialog([
        "Welcome to pyNekketsu!      Press L to continue.", 
        "Player1 controls:           arrows (to move),           K (shoot or attack),        L (pass), P (pause, start)", 
        "Player2 controls:           F, G, H, T (to move),        A (shoot or attack),        Z (pass), R (pause, start)"])

    while not dialogbox.over():
        mainClock.tick(30)
        
        Inputs.readkeys()#read all the actual keys
          
        if (Inputs.player_Esc[1] or Inputs.player_Esc[2]):
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
        if (Inputs.player_Esc[1] or Inputs.player_Esc[2]):
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
    menu_players = dialog.Menu(font, ["No human player", "Player1 VS CPU","Player1 VS Player2","Player1 + Player2 VS CPU"])
    menu_diff = dialog.Menu(font, ["too easy", "easy","medium", "hard", "too hard"])
    menu_nb_play_team = dialog.Menu(font, ["1", "2", "3", "4"])
    menu_match_length = dialog.Menu(font, ["30", "60","120", "300", "450"])

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

    while current_menu<len(menus):
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
    
    return players_human_teamA,players_human_teamB,difficulty,nb_player_team,match_length


