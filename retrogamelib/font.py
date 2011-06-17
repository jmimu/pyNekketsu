import pygame
from pygame.locals import *


class Font(object):
    
    def __init__(self, font, color=(255, 255, 255)):
        
        #Dict to hold the letter images
        self.letters = {}
        
        import os
        letters = {}
        format = " abcdefghijklmnopqrstuvwxyz0123456789-+:,.=!)(?><"
        i = 0
        self.font = font
        self.color = color
        strip = pygame.image.load(os.path.dirname(__file__) + \
            "/" + self.font["file"]).convert_alpha()
        for x in range(len(format)):
            letters[format[i]] = pygame.Surface(self.font["size"])
            letters[format[i]].blit(strip, (-x*self.font["size"][0], 0))
            i += 1
        
        #Create the letters
        for letter in letters:
            x = 0
            y = 0
            letterimg = letters[letter]
            self.letters[letter] = pygame.Surface(self.font["size"])
            self.letters[letter].set_colorkey((0, 0, 0), RLEACCEL)
            for y in range(letterimg.get_height()):
                for x in range(letterimg.get_width()):
                    if letterimg.get_at((x, y)) == (255, 255, 255, 255):
                        self.letters[letter].set_at(
                            (x, y), color
                            )
                    x += 1
                y += 1
                x = 0
    
    def render(self, text):
        text = text.lower()
        img = pygame.Surface((len(text)*self.font["size"][0], 
            self.font["size"][1]))
        img.set_colorkey((0, 0, 0), RLEACCEL)
        pos = 0
        for char in text:
            if char in self.letters:
                img.blit(self.letters[char], (pos, 0))
            pos += self.font["size"][0]
        return img

    def get_width(self):
        return self.font["size"][0]

    def get_height(self):
        return self.font["size"][1]
