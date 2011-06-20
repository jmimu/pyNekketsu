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
    nb_perso_team=1
    players_teamA=1
    players_teamB=0
    #ask for options
    dialogbox = dialog.DialogBox((240, 51), (0, 0, 0),(255, 255, 255), font)
    dialogbox.set_dialog([
        "Welcome to pyNekketsu!      Press L to continue.", 
        "Player1 controls:           arrows (to move),           K (to kick),                L (to attack)", 
        "Player2 controls:           F, G, H (to move),          A (to kick),                Z (to attack)"])
    menu_players = dialog.Menu(font, ["No human player", "Player1 VS CPU","Player1 VS Player2",
        "Player1 + Player2 VS CPU"])
    menu_diff = dialog.Menu(font, ["too easy", "easy","medium", "hard", "too hard"])
    menu_nb_play_team = dialog.Menu(font, ["1", "2","3", "4", "5"])

    menu_players_finished=False
    menu_players.move_cursor(1)
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
        elif not menu_players_finished:
            # Move the menu cursor if you press up or down    
            if Inputs.player1_just_U:
                menu_players.move_cursor(-1)
            if Inputs.player1_just_D:
                menu_players.move_cursor(1)
            # If you press A, check which option you're on!
            if Inputs.player1_just_A:
                option, text = menu_players.get_option()
                if (option==0):
                    players_teamA=0
                    players_teamB=0
                if (option==1):
                    players_teamA=1
                    players_teamB=0
                if (option==2):
                    players_teamA=1
                    players_teamB=1
                if (option==3):
                    players_teamA=2
                    players_teamB=0
                menu_players_finished=True
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
            if Inputs.player1_just_B:
                menu_players_finished=False
        else:
            # Move the menu cursor if you press up or down    
            if Inputs.player1_just_U:
                menu_nb_play_team.move_cursor(-1)
            if Inputs.player1_just_D:
                menu_nb_play_team.move_cursor(1)
            # If you press A, check which option you're on!
            if Inputs.player1_just_A:
                option, text = menu_nb_play_team.get_option()
                nb_perso_team=int(text)
                menu_nb_play_team_finished=True 
            if Inputs.player1_just_B:
                menu_diff_finished=False
        
        
        # Get the surface from the NES game library
        screen = display.get_surface()
        screen.blit(title_image,(0,0))
        
        # Draw the dialog and menu boxes
        if not dialogbox.over():
            dialogbox.draw(screen, (8, 128))
        elif not menu_players_finished:
            ren = font.render("Select game mode:")
            screen.blit(ren, (8, 112))
            menu_players.draw(screen, (16, 128), background=(0, 0, 0), border=(255, 255, 255))
        elif not menu_diff_finished:
            ren = font.render("Select game difficulty:")
            screen.blit(ren, (8, 112))
            menu_diff.draw(screen, (96, 128), background=(0, 0, 0), border=(255, 255, 255))
        else:
            ren = font.render("Number of players per team:")
            screen.blit(ren, (8, 112))
            menu_nb_play_team.draw(screen, (100, 128), background=(0, 0, 0), border=(255, 255, 255))

        # Update and draw the display
        display.update()
    
    return players_teamA,players_teamB,difficulty,nb_perso_team
