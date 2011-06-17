

class Camera(object):
    
    def __init__(self, xwindow = 80, ywindow = 80, speed = 0.05):
        self.offset = [0, 0]
        self.target = None
        self.xwindow = xwindow
        self.ywindow = ywindow
        self.speed = speed
        self.frozen = []  #Objects blocking camera from moving
    
    def follow(self, target):
        self.target = target
    
    def update(self):
        if self.frozen:
            return
        dx = self.target.rect.x-(-self.offset[0])
        if dx>80:
            self.offset[0]-=(dx-self.xwindow)*self.speed

    def translate(self, rect):
        return rect.move(self.offset)
        
    def freeze(self, object):
        if object not in self.frozen:
            self.frozen.append(object)
            
    def unfreeze(self, object):
        if object in self.frozen:
            self.frozen.remove(object)
    
    def center_at(self, pos):
        if not self.frozen:
            self.offset = list(pos)
            self.target = None
