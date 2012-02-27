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

import pygame,sys

from pygame.locals import *

from settings import configuration

#Real or fake inputs, for CPU and player
#To handle key up, keydown and joystick

class Inputs():
    #will only work with hats joystics
    print(pygame.joystick.get_count(), "joystics found.")
    joystick=[]
    if (pygame.joystick.get_count()>0):
        joystick.append(pygame.joystick.Joystick(0))
        joystick[0].init()
        print("Joystick 1 \""+joystick[0].get_name()+"\" initialized.")
    if (pygame.joystick.get_count()>1):
        joystick.append(pygame.joystick.Joystick(1))
        joystick[1].init()
        print("Joystick 2 \""+joystick[1].get_name()+"\" initialized.")
        
    player_R=[-1,False,False]
    player_L=[-1,False,False]
    player_U=[-1,False,False]
    player_D=[-1,False,False]
    player_A=[-1,False,False]
    player_B=[-1,False,False]
    player_C=[-1,False,False]
    player_Esc=[-1,False,False]
    player_Start=[-1,False,False]
    player_just_R=[-1,False,False]
    player_just_L=[-1,False,False]
    player_just_U=[-1,False,False]
    player_just_D=[-1,False,False]
    player_just_A=[-1,False,False]
    player_just_B=[-1,False,False]
    player_just_C=[-1,False,False]
    player_just_Esc=[-1,False,False]
    player_just_Start=[-1,False,False]
    
    def __init__(self, num_player_human=0):#num_player_human: to handle key configs (0=CPU)
        self.num_player_human=num_player_human
        self.R=False
        self.L=False
        self.U=False
        self.D=False
        self.A=False
        self.B=False
        self.C=False
        self.Esc=False
        self.Start=False

    def clear(self):#useful only for cpu
        self.R=False
        self.L=False
        self.U=False
        self.D=False
        self.A=False
        self.B=False
        self.C=False
        self.Esc=False
        self.Start=False



    @classmethod
    #search for the point, or create it
    def readkeys(cls):
        for i in range(1,3):
            cls.player_just_R[i]=False
            cls.player_just_L[i]=False
            cls.player_just_U[i]=False
            cls.player_just_D[i]=False
            cls.player_just_A[i]=False
            cls.player_just_B[i]=False
            cls.player_just_C[i]=False
            cls.player_just_Esc[i]=False
            cls.player_just_Start[i]=False
        
        #0 : triangle, 6 :l1,  9 : start, 11 R3_analog
        #check for joysticks
        if (len(cls.joystick)>0) and (configuration["input_p1"]=="joystick"):
            if cls.joystick[0].get_hat(0)[0]<-0.5:
                if (not cls.player_L[1]):
                    cls.player_just_L[1]=True
                cls.player_L[1] = True
            else:
                cls.player_L[1] = False
            if cls.joystick[0].get_hat(0)[0]>0.5:
                if (not cls.player_R[1]):
                    cls.player_just_R[1]=True
                cls.player_R[1] = True
            else:
                cls.player_R[1] = False
            if cls.joystick[0].get_hat(0)[1]>0.5:
                if (not cls.player_U[1]):
                    cls.player_just_U[1]=True
                cls.player_U[1] = True
            else:
                cls.player_U[1] = False
            if cls.joystick[0].get_hat(0)[1]<-0.5:
                if (not cls.player_D[1]):
                    cls.player_just_D[1]=True
                cls.player_D[1] = True
            else:
                cls.player_D[1] = False
            
            if cls.joystick[0].get_button(2):
                if (not cls.player_A[1]):
                    cls.player_just_A[1]=True
                cls.player_A[1] = True
            else:
                cls.player_A[1] = False
            if cls.joystick[0].get_button(1):
                if (not cls.player_B[1]):
                    cls.player_just_B[1]=True
                cls.player_B[1] = True
            else:
                cls.player_B[1] = False
            if cls.joystick[0].get_button(0):
                if (not cls.player_C[1]):
                    cls.player_just_C[1]=True
                cls.player_C[1] = True
            else:
                cls.player_C[1] = False
            if cls.joystick[0].get_button(9):
                if (not cls.player_Start[1]):
                    cls.player_just_Start[1]=True
                cls.player_Start[1] = True
            else:
                cls.player_Start[1] = False
        
        if (len(cls.joystick)>1) and (configuration["input_p2"]=="joystick"):
            if cls.joystick[1].get_hat(0)[0]<-0.5:
                if (not cls.player_L[2]):
                    cls.player_just_L[2]=True
                cls.player_L[2] = True
            else:
                cls.player_L[2] = False
            if cls.joystick[1].get_hat(0)[0]>0.5:
                if (not cls.player_R[2]):
                    cls.player_just_R[2]=True
                cls.player_R[2] = True
            else:
                cls.player_R[2] = False
            if cls.joystick[1].get_hat(0)[1]>0.5:
                if (not cls.player_U[2]):
                    cls.player_just_U[2]=True
                cls.player_U[2] = True
            else:
                cls.player_U[2] = False
            if cls.joystick[1].get_hat(0)[1]<-0.5:
                if (not cls.player_D[2]):
                    cls.player_just_D[2]=True
                cls.player_D[2] = True
            else:
                cls.player_D[2] = False
            
            if cls.joystick[1].get_button(2):
                if (not cls.player_A[2]):
                    cls.player_just_A[2]=True
                cls.player_A[2] = True
            else:
                cls.player_A[2] = False
            if cls.joystick[1].get_button(1):
                if (not cls.player_B[2]):
                    cls.player_just_B[2]=True
                cls.player_B[2] = True
            else:
                cls.player_B[2] = False
            if cls.joystick[1].get_button(0):
                if (not cls.player_C[2]):
                    cls.player_just_C[2]=True
                cls.player_C[2] = True
            else:
                cls.player_C[2] = False
            if cls.joystick[1].get_button(9):
                if (not cls.player_Start[2]):
                    cls.player_just_Start[2]=True
                cls.player_Start[2] = True
            else:
                cls.player_Start[2] = False

        
        # check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if (not cls.player_Esc[1]):
                        cls.player_just_Esc[1]=True
                    cls.player_Esc[1] = True
                if event.key == K_LEFT:
                    if (not cls.player_L[1]):
                        cls.player_just_L[1]=True
                    cls.player_L[1] = True
                if event.key == K_RIGHT:
                    if (not cls.player_R[1]):
                        cls.player_just_R[1]=True
                    cls.player_R[1] = True
                if event.key == K_UP:
                    if (not cls.player_U[1]):
                        cls.player_just_U[1]=True
                    cls.player_U[1] = True
                if event.key == K_DOWN:
                    if (not cls.player_D[1]):
                        cls.player_just_D[1]=True
                    cls.player_D[1] = True
                if event.key == ord('k'):
                    if (not cls.player_B[1]):
                        cls.player_just_B[1]=True
                    cls.player_B[1] = True
                if event.key == ord('l'):
                    if (not cls.player_A[1]):
                        cls.player_just_A[1]=True
                    cls.player_A[1] = True
                if event.key == ord('m'):
                    if (not cls.player_C[1]):
                        cls.player_just_C[1]=True
                    cls.player_C[1] = True
                if event.key == ord('p'):
                    if (not cls.player_Start[1]):
                        cls.player_just_Start[1]=True
                    cls.player_Start[1] = True
                if event.key == K_ESCAPE:
                    if (not cls.player_Esc[2]):   
                        cls.player_just_Esc[2]=True
                    cls.player_Esc[2] = True
                if event.key == ord('f'):
                    if (not cls.player_L[2]):   
                        cls.player_just_L[2]=True
                    cls.player_L[2] = True
                if event.key == ord('h'):
                    if (not cls.player_R[2]):   
                        cls.player_just_R[2]=True
                    cls.player_R[2] = True
                if event.key == ord('t'):
                    if (not cls.player_U[2]):   
                        cls.player_just_U[2]=True
                    cls.player_U[2] = True
                if event.key == ord('g'):
                    if (not cls.player_D[2]):   
                        cls.player_just_D[2]=True
                    cls.player_D[2] = True
                if event.key == ord('a'):
                    if (not cls.player_B[2]):   
                        cls.player_just_B[2]=True
                    cls.player_B[2] = True
                if event.key == ord('z'):
                    if (not cls.player_A[2]):   
                        cls.player_just_A[2]=True
                    cls.player_A[2] = True
                if event.key == ord('e'):
                    if (not cls.player_C[2]):   
                        cls.player_just_C[2]=True
                    cls.player_C[2] = True
                if event.key == ord('r'):
                    if (not cls.player_Start[2]):   
                        cls.player_just_Start[2]=True
                    cls.player_Start[2] = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    cls.player_Esc[1] = False
                if event.key == K_LEFT:
                    cls.player_L[1] = False
                if event.key == K_RIGHT:
                    cls.player_R[1] = False
                if event.key == K_UP:
                    cls.player_U[1] = False
                if event.key == K_DOWN:
                    cls.player_D[1] = False
                if event.key == ord('k'):
                    cls.player_B[1] = False
                if event.key == ord('l'):
                    cls.player_A[1] = False
                if event.key == ord('m'):
                    cls.player_C[1] = False
                if event.key == ord('p'):
                    cls.player_Start[1] = False
                if event.key == K_ESCAPE:
                    cls.player_Esc[2] = False
                if event.key == ord('f'):
                    cls.player_L[2] = False
                if event.key == ord('h'):
                    cls.player_R[2] = False
                if event.key == ord('t'):
                    cls.player_U[2] = False
                if event.key == ord('g'):
                    cls.player_D[2] = False
                if event.key == ord('a'):
                    cls.player_B[2] = False
                if event.key == ord('z'):
                    cls.player_A[2] = False
                if event.key == ord('e'):
                    cls.player_C[2] = False
                if event.key == ord('r'):
                    cls.player_Start[2] = False


    def update(self):#read corresponding key for human player, of just release keys for CPU
        if (self.num_player_human==1):#it won't work this way... have to hanlde all events at the same time, instead they are lost (won't work with 2 players)
            self.R=Inputs.player_R[1]
            self.L=Inputs.player_L[1]
            self.U=Inputs.player_U[1]
            self.D=Inputs.player_D[1]
            self.A=Inputs.player_A[1]
            self.B=Inputs.player_B[1]
            self.C=Inputs.player_C[1]
            self.Esc=Inputs.player_Esc[1]
            self.Start=Inputs.player_Start[1]
        if (self.num_player_human==2):#it won't work this way... have to hanlde all events at the same time, instead they are lost (won't work with 2 players)
            self.R=Inputs.player_R[2]
            self.L=Inputs.player_L[2]
            self.U=Inputs.player_U[2]
            self.D=Inputs.player_D[2]
            self.A=Inputs.player_A[2]
            self.B=Inputs.player_B[2]
            self.C=Inputs.player_C[2]
            self.Esc=Inputs.player_Esc[2]
            self.Start=Inputs.player_Start[2]
                    
        if (self.num_player_human==0):#CPU: the inputs are trigged in PlayerCPU code
            self.R=False
            self.L=False
            self.U=False
            self.D=False
            self.A=False
            self.B=False
            self.C=False
            self.Esc=False
            self.Start=False
                    

