import pygame

def arrow_image(color):
    img = pygame.Surface((7, 6))
    img.fill((226, 59, 252))
    img.set_colorkey((226, 59, 252), pygame.RLEACCEL)
    pygame.draw.polygon(img, color, ((0, 0), (3, 3), (6, 0)))
    return img

class Menu(object):
    
    def __init__(self, font, options):
        self.font = font
        self.options = options
        self.option = 0
        self.height = len(self.options)*(self.font.get_height())+(len(self.options)-1)*3
        self.width = 0
        for o in self.options:
            w = (len(o)+1)*self.font.get_width()
            if w > self.width:
                self.width = w
    
    def draw(self, surface, pos, background=None, border=None):
        ypos = pos[1]
        i = 0
        if background:
            pygame.draw.rect(surface, background, (pos[0]-4, pos[1]-4, 
                self.width+8, self.height+6))
        if border:
            pygame.draw.rect(surface, border, (pos[0]-4, pos[1]-4, 
                self.width+8, self.height+8), 1)
        for opt in self.options:
            if i == self.option:
                icon = ">"
            else:
                icon = " "
            ren = self.font.render(icon + opt)
            surface.blit(ren, (pos[0], ypos))
            ypos += ren.get_height()+3
            i += 1
    
    def move_cursor(self, dir):
        if dir > 0:
            if self.option < len(self.options)-1:
                self.option += 1
        elif dir < 0:
            if self.option > 0:
                self.option -= 1
    
    def get_option(self):
        return self.option, self.options[self.option]

class DialogBox(object):
    
    def __init__(self, size, background_color, border_color, font):
        self.dialog = []
        self.image = pygame.Surface(size)
        self.font = font
        self.size = size
        self.background_color = background_color
        self.border_color = border_color
        self.update_box()
        self.text_pos = 0
        self.shown = False
        self.scroll_delay = 1
        self.frame = 0
        self.down_arrow = arrow_image(font.color)
        self.curr_dialog=0
    
    def set_scrolldelay(self, delay):
        self.scroll_delay = delay
    
    def set_dialog(self, dialog_list):
        self.page = 0
        self.pages = len(dialog_list)
        self.dialog = dialog_list
        self.shown = True
        self.text_pos = 0
    
    def update_box(self):
        self.image.fill(self.background_color)
        pygame.draw.rect(self.image, self.border_color, 
            (0, 0, self.size[0]-1, self.size[1]-1), 1)
    
    def progress(self):
        if (self.curr_dialog==0):
            return
        if (self.text_pos >= len(self.curr_dialog)):
            if self.page < self.pages-1:
                self.page += 1
                self.text_pos = 0
            else:
                self.shown = False
        else:
            self.text_pos = len(self.curr_dialog)
    
    def draw(self, surface, pos):
        if self.shown and self.page < self.pages:
            self.update_box()
            self.curr_dialog = self.dialog[self.page]
            xpos = 4
            ypos = 4
            if self.text_pos < len(self.curr_dialog):
                self.frame -= 1
                if self.frame <= 0:
                    self.text_pos += 1
                    self.frame = self.scroll_delay
            else:
                self.image.blit(self.down_arrow, 
                    (self.image.get_width()-12, 
                    self.image.get_height()-8))
            dialog = self.curr_dialog[:self.text_pos]
            for word in dialog.split(" "):
                ren = self.font.render(word + " ")
                w = ren.get_width()
                if xpos > self.image.get_width()-w:
                    ypos += ren.get_height()+3
                    xpos = 4
                self.image.blit(ren, (xpos, ypos))
                xpos += w
            surface.blit(self.image, pos)
    
    def over(self):
        return self.shown != True
    
    def close(self):
        self.shown = False
        self.page = self.pages
