#! /usr/bin/python


import pygame
import os
import random
from perso import Perso

class PersoCPU(Perso):
    
    def __init__(self):
        Perso.__init__(self)
        
    def update(self,match):
        Perso.update(self,match) 

