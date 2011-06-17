import math

class Vector:
   
    def __init__(self, x, y):
        self.x, self.y = x, y
        
    def __repr__(self):
        return "Vector(%s, %s)"%(self.x, self.y)
   
    def copy(self):
        return Vector(self.x, self.y)
   
    def dot(self, other):
        return self.x*other.x + self.y*other.y
   
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
   
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __sub__(self, other):
        return -other + self
   
    def __mul__(self, scalar):
        return Vector(self.x*scalar, self.y*scalar)
  
    __rmul__ = __mul__
    def __div__(self, scalar):
        return 1.0/scalar * self
        
    def angle(self):
        return math.degrees(math.atan2(self.y, self.x))
        
    def rotate(self, ang):
        ang = self.angle()+ang
        mag = self.magnitude()
        x = math.cos(math.radians(ang)) * mag
        y = math.sin(math.radians(ang)) * mag
        return Vector(x, y)
    
    def magnitude(self):
        return math.sqrt(self.x*self.x + self.y*self.y)
 
    def normalize(self):
        inverse_magnitude = 1.0/self.magnitude()
        return Vector(self.x*inverse_magnitude, self.y*inverse_magnitude)
 
    def perpendicular(self):
        return Vector(-self.y, self.x)
 
class Projection:
    
    def __init__(self, min, max):
        self.min, self.max = min, max
   
    def intersection(self, other):
        if self.max > other.min and other.max > self.min:
            return self.max-other.min
        return 0
 
class Polygon:
   
    def __init__(self, pos, points):
        if type(pos) in [type(()), type([])]:
            self.pos = Vector(pos[0], pos[1])
        elif isinstance(pos, Vector):
            self.pos = pos
        else:
            raise SystemExit, "Illegal type for pos."
        self.points = []
        for p in points:
            self.points.append(Vector(*p))
        
        self.edges = []
        for i in range(len(self.points)):
            point = self.points[i]
            next_point = self.points[(i+1)%len(self.points)]
            self.edges.append(next_point - point)
    
    def __getitem__(self, i):
        return self.points[i]
    
    def __iter__(self):
        return iter(self.points)
    
    def get_points(self):
        new_points = []
        for point in self.points:
            p = point.copy()
            p.x += self.pos.x
            p.y += self.pos.y
            new_points.append((p.x, p.y))
        return new_points
    
    def project_to_axis(self, axis):
        projected_points = []
        for point in self.points:
            p = point.copy()
            p.x += self.pos.x
            p.y += self.pos.y
            projected_points.append(p.dot(axis))
        return Projection(min(projected_points), max(projected_points))
  
    def intersects(self, other):
        edges = []
        edges.extend(self.edges)
        edges.extend(other.edges)
        
        projections = []
        for edge in edges:
            axis = edge.normalize().perpendicular()
            
            self_projection = self.project_to_axis(axis)
            other_projection = other.project_to_axis(axis)
            intersection1 = self_projection.intersection(other_projection)
            intersection2 = -other_projection.intersection(self_projection)
            if not intersection1:
                return False
                
            proj_vector1 = Vector(axis.x*intersection1,axis.y*intersection1)
            proj_vector2 = Vector(axis.x*intersection2,axis.y*intersection2)
            projections.append(proj_vector1)
            projections.append(proj_vector2)
        
        mtd = -self.find_mtd(projections)
        
        return mtd
    
    def collide(self, other):
        mtd = self.intersects(other)
        if mtd:
            self.pos += mtd
    
    def find_mtd(self, push_vectors):
        mtd = push_vectors[0]
        mind2 = push_vectors[0].dot(push_vectors[0])
        for vector in push_vectors[1:]:
            d2 = vector.dot(vector)
            if d2 < mind2:
                mind2 = d2
                mtd = vector
        return mtd

class Rect(Polygon):
    
    def __init__(self, x, y, w, h):
        points = [(0, 0), (w, 0), (w, h), (0, h)]
        Polygon.__init__(self, (x, y), points)
        self.width = w
        self.height = h
