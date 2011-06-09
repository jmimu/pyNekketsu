#! /usr/bin/python

import pygame,sys

from pygame.locals import *

#Real or fake inputs, for CPU and player
#To handle key up, keydown and joystick

class Inputs():
    player1_R=False
    player1_L=False
    player1_U=False
    player1_D=False
    player1_A=False
    player1_B=False
    player1_C=False
    player1_Esc=False
    player2_R=False
    player2_L=False
    player2_U=False
    player2_D=False
    player2_A=False
    player2_B=False
    player2_C=False
    player2_Esc=False
    
    def __init__(self, num_player=0):#num_player: to handle key configs (0=CPU)
        self.num_player=num_player
        self.R=False
        self.L=False
        self.U=False
        self.D=False
        self.A=False
        self.B=False
        self.C=False
        self.Esc=False
    
    @classmethod
    #search for the point, or create it
    def readkeys(cls):
        # check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    cls.player1_Esc = True
                if event.key == K_LEFT:
                    cls.player1_L = True
                if event.key == K_RIGHT:
                    cls.player1_R = True
                if event.key == K_UP:
                    cls.player1_U = True
                if event.key == K_DOWN:
                    cls.player1_D = True
                if event.key == ord('w'):
                    cls.player1_B = True
                if event.key == ord('x'):
                    cls.player1_A = True
                if event.key == ord('c'):
                    cls.player1_C = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    cls.player1_Esc = False
                if event.key == K_LEFT:
                    cls.player1_L = False
                if event.key == K_RIGHT:
                    cls.player1_R = False
                if event.key == K_UP:
                    cls.player1_U = False
                if event.key == K_DOWN:
                    cls.player1_D = False
                if event.key == ord('w'):
                    cls.player1_B = False
                if event.key == ord('x'):
                    cls.player1_A = False
                if event.key == ord('c'):
                    cls.player1_C = False

    def update(self):#read corresponding key for human player, of just release keys for CPU
        if (self.num_player==1):#it won't work this way... have to hanlde all events at the same time, instead they are lost (won't work with 2 players)
            self.R=Inputs.player1_R
            self.L=Inputs.player1_L
            self.U=Inputs.player1_U
            self.D=Inputs.player1_D
            self.A=Inputs.player1_A
            self.B=Inputs.player1_B
            self.C=Inputs.player1_C
            self.Esc=Inputs.player1_Esc
        if (self.num_player==2):#it won't work this way... have to hanlde all events at the same time, instead they are lost (won't work with 2 players)
            self.R=Inputs.player2_R
            self.L=Inputs.player2_L
            self.U=Inputs.player2_U
            self.D=Inputs.player2_D
            self.A=Inputs.player2_A
            self.B=Inputs.player2_B
            self.C=Inputs.player2_C
            self.Esc=Inputs.player2_Esc
                    
        if (self.num_player==0):#CPU: the inputs are trigged in PlayerCPU code
            self.R=False
            self.L=False
            self.U=False
            self.D=False
            self.A=False
            self.B=False
            self.C=False
            self.Esc=False
                    

