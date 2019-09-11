from math import pi, sin, cos
# TODO use these two classes everywhere, instead of just tuples
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


def rotate_vector(vector, degrees):
    deg_to_rad = pi/180
    rads = degrees * deg_to_rad
    cosine = cos(rads)
    sinus = sin(rads)
    # Vector(ca*v.X - sa*v.Y, sa*v.X + ca*v.Y)
    return cosine * vector[0] - sinus * vector[1], sinus * vector[0] + cosine * vector[1]


def t_hit(line, particle, direction):
    """Calculates the time it takes for a particle to hit a line, given a direction.
       line is two points, particle is a point, direction is a vector."""
    # The formula is (normal . (p1 - particle))/(normal . direction)
    # Get the two points of the line
    p1, p2 = line
    # Make the points into a vector
    p2p1 = p2 - p1
    # Get the normal of the vector
    n = Vector(p2p1.y, -p2p1.x)
    # Vector from the particle to a point we know is on the line
    p1particle = p1 - particle
    p1particle = Vector(p1particle.x, p1particle.y)
    # pow is overloaded to be dot product
    # tried overloading mul but didn't take for some reason.
    above = n ** p1particle
    below = n ** direction
    # Direction is parallel to the line, will never in a million years hit
    if below == 0:
        return -1
    # print("p1: {}; p2: {}; particle: {}; direction: {}; normal: {}; above: {}; below: {}".format(p1, p2, particle,
    # direction, n, above, below))

    return above / below


def p_hit(particle, time_to_hit, direction):
    """Calculates where a particle will be in some time, given a direction.
       Particle is a point, t_hit from the t_hit function, direction is a vector."""
    # Formula is particle + t_hit * direction
    tmp = Point(direction.x * time_to_hit, direction.y * time_to_hit)
    return particle + tmp


def reflect(direction, line):
    """Reflects a direction vector about a line"""
    # The formula is: direction - 2(direction . normal)/(normal . normal) * normal
    # Get the normal of the line
    p1, p2 = line
    p2p1 = p2 - p1
    n = Vector(p2p1.y, -p2p1.x)
    # Calculate the inner brackets
    cn = direction ** n
    # Outer brackets
    cn *= 2
    # Divide, since I'm too lazy to make a normalize function
    cn /= n ** n
    # Multiply by the normal
    cn = Point(cn * n.x, cn * n.y)
    # Last bit of the formula
    return direction - cn

# t = t_hit((Point(3,8), Point(7,6)), Point(4,2), Vector(1, 3))
# p = p_hit(Point(4,2), t, Vector(1, 3))
# print(t, p)
# print(reflect(Vector(1,3), (Point(3,8), Point(7,6))))
