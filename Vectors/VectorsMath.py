import math

class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, v):
        return [self.x + v[0], self.y + v[1]]

    def sub(self, v):
        return [self.x - v[0], self.y - v[1]]

    def mult(self, s):
        return [self.x * s, self.y * s]

    def div(self, s):
        return [self.x / s, self.y / s]

    def mag(self):
        return (self.x**2 + self.y**2)**0.5

    def normalize(self):
        mag = self.mag()
        if mag != 0:
            self.x /= mag
            self.y /= mag

    def rotate(self, angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        new_x = self.x * cos - self.y * sin
        new_y = self.x * sin + self.y * cos
        self.x = new_x
        self.y = new_y

    def lerp(self, v, a):
        return self.y + ((a-self.x)*(v[1]-self.y)/ (v[0]-self.x))

    def dist(self, v):
        return ((self.x - v[0])**2 + (self.y - v[1])**2)**0.5

    def angleBetween(self, v):
        return math.acos(self.dot(v) / (self.mag() * (v[0]**2 + v[1]**2)**0.5))

    def dot(self,v):
        return self.x * v[0] + self.y * v[1]

class Vector3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def add(self, v):
        return [self.x + v[0], self.y + v[1], self.z + v[2]]

    def sub(self, v):
        return [self.x - v[0], self.y - v[1], self.z - v[2]]

    def mult(self, s):
        return [self.x * s, self.y * s, self.z * s]

    def div(self, s):
        return [self.x / s, self.y / s, self.z / s]

    def mag(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def normalize(self):
        mag = self.mag()
        if mag != 0:
            self.x /= mag
            self.y /= mag
            self.z /= mag

    def rotateX(self, angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        new_y = self.y * cos - self.z * sin
        new_z = self.y * sin + self.z * cos
        self.y = new_y
        self.z = new_z

    def rotateY(self, angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        new_x = self.x * cos + self.z * sin
        new_z = -self.x * sin + self.z * cos
        self.x = new_x
        self.z = new_z

    def rotateZ(self, angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        new_x = self.x * cos - self.y * sin
        new_y = self.x * sin + self.y * cos
        self.x = new_x
        self.y = new_y

    def lerp(self, v, a):
            x = self.x + (v[0] - self.x) * a
            y = self.y + (v[1] - self.y) * a
            z = self.z + (v[2] - self.z) * a
            return [x, y, z]
        
    def dist(self, v):
        return ((self.x - v[0])**2 + (self.y - v[1])**2 + (self.z - v[2])**2)**0.5

    def angleBetween(self, v):
        return self.dot(v) /  (self.mag() * (v[0]**2 + v[1]**2 + v[2]**2)**0.5)

    def dot(self,v):
        return self.x * v[0] + self.y * v[1] + self.z * v[2]