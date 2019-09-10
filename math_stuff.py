class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other): 
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __str__(self):
        return "({}, {})".format(self.x, self.y)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other): 
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, c):
        return Vector(self.x * c, self.y * c)

    def __pow__(self, other):
        return self.x * other.x + self.y * other.y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)
    
def t_hit(line, particle, direction):
    """line is two points, particle is a point, direction is a vector."""
    p1, p2 = line
    p2p1 = p2 - p1
    n = Vector(p2p1.y, -p2p1.x)
    p1particle = p1 - particle
    p1particle = Vector(p1particle.x, p1particle.y)
    above = n ** p1particle
    below = n ** direction
    return above/below


def p_hit(particle, t_hit, direction):
    tmp = Point(direction.x * t_hit, direction.y * t_hit)
    return particle + tmp

# t = t_hit((Point(3,8), Point(7,6)), Point(4,2), Vector(1, 3))
# p = p_hit(Point(4,2), t, Vector(1, 3))
# print(t, p)
