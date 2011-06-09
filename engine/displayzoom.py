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

# modified form RetroGameLib: http://code.google.com/p/retrogamelib/

import sys
import os

import pygame
from pygame.locals import *


class DisplayZoom():
    def __init__(self,_scale, _caption, _resX, _resY):
        """Initialise the SDL display -> return None
        """
        self.scale=_scale
        self.caption=_caption
        self.resX=_resX
        self.resY=_resY
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        
        pygame.display.set_caption(_caption)
        self.screen = pygame.display.set_mode((int(self.resX*self.scale),int(self.resY*self.scale)))
        self.surface = pygame.Surface([self.resX,self.resY])
        self.update()
        
        pygame.mouse.set_visible(0)
    
    def update(self):
        """Update and draw the scene -> return None
        """
        
        self.surface = pygame.transform.scale(self.surface,(int(self.resX*self.scale), int(self.resY*self.scale)))
        self.screen.blit(self.surface, (0, 0))
        self.surface = pygame.transform.scale(self.surface, [self.resX,self.resY])
        pygame.display.flip()
    
    
    def get_surface(self):
        """Get the surface to draw to -> return pygame.Surface
        """
        
        return self.surface
