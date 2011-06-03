#! /usr/bin/python


import pygame
import os
import random
from perso import Perso
from inputs import Inputs

class PersoPlayer(Perso):
    
    def __init__(self):
        Perso.__init__(self)
        self.inputs=Inputs(1) #key config: player 1
        
    def update(self,match):
        Perso.update(self,match) 



