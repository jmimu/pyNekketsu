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


def call_menu(display,font,mainClock):
    difficulty=5
    nb_player_team=1
    #ask for options
    dialogbox = dialog.DialogBox((240, 51), (0, 0, 0),(255, 255, 255), font)
    dialogbox.set_dialog([
        "Welcome to pyNekketsu!      Press L to continue.", 
        "Please select difficulty and number of persos per team.      Press L to continue."])
    menu_diff = dialog.Menu(font, ["too easy", "easy","medium", "hard", "too hard"])
    menu_nb_play_team = dialog.Menu(font, ["1", "2","3", "4", "5"])

    menu_diff_finished=False
    menu_nb_play_team_finished=False
    title_image=pygame.image.load("data/title.png")
    
    while not menu_nb_play_team_finished:
        mainClock.tick(30)
        
        Inputs.readkeys()#read all the actual keys
          
        if (Inputs.player1_Esc or Inputs.player2_Esc):
            pygame.quit()
            sys.exit()

        # If displaying dialog, do events for dialog!
        if not dialogbox.over():
            if Inputs.player1_just_A:
                dialogbox.progress()
        elif not menu_diff_finished:
            # Move the menu cursor if you press up or down    
            if Inputs.player1_just_U:
                menu_diff.move_cursor(-1)
            if Inputs.player1_just_D:
                menu_diff.move_cursor(1)
            # If you press A, check which option you're on!
            if Inputs.player1_just_A:
                option, text = menu_diff.get_option()
                difficulty=2+option*2
                menu_diff_finished=True
        else:
            # Move the menu cursor if you press up or down    
            if Inputs.player1_just_U:
                menu_nb_play_team.move_cursor(-1)
            if Inputs.player1_just_D:
                menu_nb_play_team.move_cursor(1)
            # If you press A, check which option you're on!
            if Inputs.player1_just_A:
                option, text = menu_nb_play_team.get_option()
                nb_player_team=int(text)
                menu_nb_play_team_finished=True 
        
        
        # Get the surface from the NES game library
        screen = display.get_surface()
        screen.blit(title_image,(0,0))
        
        # Draw the dialog and menu boxes
        if not dialogbox.over():
            dialogbox.draw(screen, (8, 128))
        elif not menu_diff_finished:
            ren = font.render("Select game difficulty:")
            screen.blit(ren, (8, 112))
            menu_diff.draw(screen, (96, 128), background=(0, 0, 0), border=(255, 255, 255))
        else:
            ren = font.render("Number of persos per team:")
            screen.blit(ren, (8, 112))
            
            menu_nb_play_team.draw(screen, (96, 128), background=(0, 0, 0), border=(255, 255, 255))

        # Update and draw the display
        display.update()
    
    return difficulty,nb_player_team
