import pygame
import os

def filepath(path):
    if "/" in path:
        path = path.split("/")
    elif "\\" in path:
        path = path.split("\\")
    if type(path) is type([]):
        return os.path.join(*path)
    else:
        return os.path.join(path)

IMAGES = {}
def load_image(filename):
    if filename not in IMAGES:
        IMAGES[filename] = pygame.image.load(
            filepath(filename)).convert_alpha()
    return IMAGES[filename]

def play_music(filename, loop=0, volume=1.0):
    pygame.mixer.music.load(filepath(filename))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loop)

SOUNDS = {}
SND_VOLUME = 1.0
def play_sound(filename, volume=1.0):
    if filename not in SOUNDS:
        SOUNDS[filename] = pygame.mixer.Sound(filepath(filename))
        SOUNDS[filename].set_volume(SND_VOLUME*volume)
    SOUNDS[filename].play()

def set_global_sound_volume(volume):
    global SND_VOLUME
    SND_VOLUME = volume
