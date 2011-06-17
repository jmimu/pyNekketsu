class Object(object):
    
    def __init__(self, groups):
        for group in groups:
            group.add(self)
        self._groups = groups
        self.z = 0
    
    def alive(self):
        return self._groups != []
    
    def kill(self):
        for g in self.groups:
            g.remove(self)
        self._groups = []
    
    def update(self):
        pass
    
    def draw(self, surface):
        pass

class Group(object):
    
    def __init__(self):
        self._objects = []
    
    def __len__(self):
        return len(self._objects)
    
    def __iter__(self):
        return iter(sorted(self._objects, key=lambda x: x.z))
    
    def __getitem__(self, index):
        return self._objects[index]
    
    def objects(self):
        return sorted(self._objects, key=lambda x: x.z)
    
    def add(self, object):
        if object not in self._objects:
            self._objects.append(object)
    
    def remove(self, object):
        if object in self._objects:
            self._objects.remove(object)
        
