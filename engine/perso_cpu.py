#! /usr/bin/python


import pygame
import os
import random
from perso import Perso
from inputs import Inputs

difficulty=8 #out of 10


class PersoCPU(Perso):
    
    def __init__(self,team):
        Perso.__init__(self,team)
        self.inputs=Inputs(0)
        
    def update(self,match):
        Perso.update(self,match) 
        self.think(match)

    def think(self,match):#press on virtual keys
        if (self.has_ball!=0):
            #look in the goal's direction
            if (self.team.wing==1):
                self.inputs.R=True
            else:
                self.inputs.L=True
            if (match.field.goal_latitude[self.team.wing]-10>self.pos[1]) or (random.randint(0, 4)==0):
                self.inputs.U=True
            if (match.field.goal_latitude[self.team.wing]+10<self.pos[1]) or (random.randint(0, 4)==0):
                self.inputs.D=True
            #shoot!
            if (random.randint(0, int(abs(self.team.wing*match.field.half_length-self.pos[0])))==0):#depends on the distance to the goal
                self.inputs.B=True
        else:
            if (self.pos[0]<match.ball.pos[0]-2) and (random.randint(0, 20)<10+difficulty):
                self.inputs.R=True
            if (self.pos[0]>match.ball.pos[0]+2) and (random.randint(0, 20)<10+difficulty):
                self.inputs.L=True
            if (self.pos[1]<match.ball.pos[1]-5) and (random.randint(0, 20)<10+difficulty):
                self.inputs.U=True
            if (self.pos[1]>match.ball.pos[1]+5) and (random.randint(0, 20)<10+difficulty):
                self.inputs.D=True
            for p in match.perso_list:
                if (p!=self):
                    if (p.team!=self.team):#attack!
                        if (abs(p.pos[0]-self.pos[0])<5 and abs(p.pos[1]-self.pos[1])<5):
                            if (random.randint(0, 80)==0) or (p.has_ball!=0):
                                self.inputs.A=True
                
