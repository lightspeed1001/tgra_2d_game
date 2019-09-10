from OpenGLWrapper import *
from constants import *

class GameObject(object):
    """This is the base object for all the object in the game, such as enemies, player, etc."""
    def __init__(self, x, y, vertices, color):
        """Initialize the object"""
        self.x = x
        self.y = y
        self.vertices = vertices
        self.color = color

    def __iter__(self):
        yield self

    def move(self, direction, delta_time):
        """Move the object."""
        self.x += direction[0] * delta_time
        self.y += direction[1] * delta_time

    def update(self, delta_time):
        """Does any update logic. This basic function does nothing. Please override. """
        pass

    def collision_check(self, other):
        """Checks if the object collides with other."""
        pass

    def draw(self):
        """Draw self."""
        draw_poly(self.x, self.y, self.vertices, self.color)


class Player(GameObject):
    """The player object"""
    def __init__(self, x, y, vertices, color, hp, shields, lives):
        super().__init__(x, y, vertices, color)
        self.hp = hp
        self.shields = shields
        self.lives = lives
        
    def draw(self):
        """Draw self."""
        draw_poly(self.x, self.y, self.vertices, self.color, GL_TRIANGLE_STRIP)

    def shoot(self):
        """Shoots a projectile straight."""
        new_bullet = Bullet(self.x, self.y + 12, (0,0), COLOR_BULLET, BULLET_UP)
        return new_bullet

    def take_damage(self, damage, type):
        """Take some damage."""
        pass

    def die(self):
        """Lose a life and stuff."""
        pass


class Enemy(GameObject):
    """Base enemy object"""
    def __init__(self, x, y, vertices, color, hp, shields):
        super().__init__(x, y, vertices, color)
        self.hp = hp
        self.shields = shields

    def shoot(self, direction):
        """Shoots in a direction."""
        pass
    
    def update(self, delta_time):
        """Does any update logic. This basic function does nothing. Please override. """
        self.y -= delta_time * ENEMY_SPEED
        pass

    def die(self):
        """Does any cleanup required."""
        pass

    def draw(self):
        """Draw self."""
        draw_poly(self.x, self.y, self.vertices, self.color, GL_TRIANGLE_STRIP)


class Bullet(GameObject):
    """Basic bullet object."""
    def __init__(self, x, y, vertices, color, direction, hp_damage=1, shield_damage=1):
        super().__init__(x, y, vertices, color)
        self.direction = direction
        self.hp_damage = hp_damage
        self.shield_damage = shield_damage

    def draw(self):
        """Draw self."""
        draw_point(self.x, self.y, 5, self.color)

    def update(self, delta_time):
        self.x += self.direction[0] * delta_time
        self.y += self.direction[1] * delta_time

class Wall(GameObject):
    """Some basic walls and stuff."""
    def draw(self):
        """Draw self."""
        draw_poly(self.x, self.y, self.vertices, self.color, GL_LINE_LOOP)

    def update(self, delta_time):
        """Does any update logic. This basic function does nothing. Please override. """
        self.y -= delta_time * SCROLL_SPEED