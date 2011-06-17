import sys
import os

import pygame
from pygame.locals import *

from constants import *

SCALE  = 1.0
screen = None
surface = None
resolution = None

def init(scale=2.0, caption="NES Game", res=NESRES):
    """Initialise the SDL display -> return None
    """
    
    global SCALE, screen, surface, resolution
    resolution = res
    SCALE = scale
    
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    
    pygame.display.set_caption(caption)
    screen = pygame.display.set_mode((
        int(resolution[0]*SCALE), 
        int(resolution[1]*SCALE)))
    surface = pygame.Surface(NESRES)
    update()
    
    pygame.mouse.set_visible(0)

def update():
    """Update and draw the scene -> return None
    """
    
    global surface, resolution
    surface = pygame.transform.scale(surface, 
        (int(resolution[0]*SCALE), int(resolution[1]*SCALE)))
    screen.blit(surface, (0, 0))
    surface = pygame.transform.scale(surface, resolution)

    pygame.display.flip()

def get_surface():
    """Get the surface to draw to -> return pygame.Surface
    """
    
    return surface
