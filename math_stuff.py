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
    """Calculates the time it takes for a particle to hit a line, given a direction.
       line is two points, particle is a point, direction is a vector."""
    p1, p2 = line
    p2p1 = p2 - p1
    n = Vector(p2p1.y, -p2p1.x)
    p1particle = p1 - particle
    p1particle = Vector(p1particle.x, p1particle.y)
    above = n ** p1particle
    below = n ** direction
    return above/below


def p_hit(particle, t_hit, direction):
    """Calculates where a particle will be in some time, given a direction.
       Particle is a point, t_hit from the t_hit function, direction is a vector."""
    tmp = Point(direction.x * t_hit, direction.y * t_hit)
    return particle + tmp


def reflect(direction, line):
    """Reflects a direction vector about a line"""
    p1, p2 = line
    p2p1 = p2 - p1
    n = Vector(p2p1.y, -p2p1.x)

    cn = direction ** n
    cn *= 2
    cn /= n ** n
    cn = Point(cn * n.x, cn * n.y)

    return direction - cn
# t = t_hit((Point(3,8), Point(7,6)), Point(4,2), Vector(1, 3))
# p = p_hit(Point(4,2), t, Vector(1, 3))
# print(t, p)
# print(reflect(Vector(1,3), (Point(3,8), Point(7,6))))
