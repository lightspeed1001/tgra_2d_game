from OpenGLWrapper import *
from constants import *
from math_stuff import *


class GameObject(object):
    """This is the base object for all the object in the game, such as enemies, player, etc."""

    def __init__(self, x, y, vertices, color):
        """Initialize the object"""
        self.x = x
        self.y = y
        self.vertices = vertices
        self.color = color
        self.alive = True

    def __iter__(self):
        yield self

    def move(self, direction, delta_time):
        """Move the object."""
        self.x += direction[0] * delta_time
        self.y += direction[1] * delta_time

    def update(self, delta_time):
        """Does any update logic. This basic function does nothing. Please override. """
        pass

    def collision_check(self, other, delta_time):
        """Checks if the object collides with other."""
        pass

    def draw(self):
        """Draw self."""
        draw_poly(self.x, self.y, self.vertices, self.color)

    def destroy(self):
        """Sets cleanup flag"""
        self.alive = False


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
        new_bullet = Bullet(self.x, self.y + 26, (0, 0), COLOR_BULLET, BULLET_UP)
        return new_bullet

    def take_damage(self, hp_dmg, sh_dmg):
        """Take some damage."""
        if self.shields <= 0:
            self.hp = max(0, self.hp - hp_dmg)
        else:
            self.shields = max(0, self.shields - sh_dmg)
        if self.hp <= 0:
            self.die()

    def die(self):
        """Lose a life and stuff."""
        # TODO Some proper game-over stuff
        self.destroy()


class Enemy(GameObject):
    """Base enemy object"""

    def __init__(self, x, y, vertices, color, hp, shields):
        super().__init__(x, y, vertices, color)
        self.hp = hp
        self.shields = shields

    def shoot(self, direction):
        """Shoots in a direction."""
        new_bullet = Bullet(self.x, self.y - 7, (0, 0), COLOR_BULLET, direction)
        return new_bullet

    def update(self, delta_time):
        """Does any update logic. This basic function does nothing. Please override. """
        self.y -= delta_time * ENEMY_SPEED
        pass

    def die(self):
        """Does any cleanup required."""
        # TODO some proper death stuff
        self.destroy()

    def draw(self):
        """Draw self."""
        draw_poly(self.x, self.y, self.vertices, self.color, GL_TRIANGLE_STRIP)

    def take_damage(self, hp_dmg, sh_dmg):
        """Take some damage."""
        # print("Enemy taking damage")
        if self.shields <= 0:
            self.hp = max(0, self.hp - hp_dmg)
        else:
            self.shields = max(0, self.shields - sh_dmg)
        if self.hp <= 0:
            # print("Enemy should die")
            self.die()
        # print(self.hp, self.shields)


class Bullet(GameObject):
    """Basic bullet object."""

    def __init__(self, x, y, vertices, color, direction, hp_damage=1, shield_damage=1, bounces=2):
        super().__init__(x, y, vertices, color)
        self.direction = direction
        self.hp_damage = hp_damage
        self.shield_damage = shield_damage
        self.bounces = bounces

    def draw(self):
        """Draw self."""
        draw_point(self.x, self.y, 5, self.color)

    def update(self, delta_time):
        self.x += self.direction[0] * delta_time
        self.y += self.direction[1] * delta_time

    def collision_check(self, other, delta_time):
        """Checks if the object collides with other."""
        # This is just a particle, so we can use the math_stuff thingy
        self_point = Point(self.x, self.y)
        self_direction = Vector(self.direction[0], self.direction[1])

        previous_line_point = other.vertices[0]
        previous_line_point = Point(other.x - previous_line_point[0], other.y + previous_line_point[1])

        # print(self_point)
        # print(previous_line_point)
        # exit()
        for line_point in other.vertices[1:]:
            new_point = Point(other.x - line_point[0], other.y + line_point[1])

            line = (previous_line_point, new_point)
            time_to_hit = t_hit(line, self_point, self_direction)

            if delta_time >= time_to_hit >= 0:
                # print("p1: {}; p2: {}".format(previous_line_point, new_point))
                where_hit = p_hit(self_point, time_to_hit, self_direction)
                # print(where_hit)
                if new_point.x <= where_hit.x <= previous_line_point.x or previous_line_point.x <= where_hit.x <= new_point.x:
                    if isinstance(other, Wall):
                        new_direction = reflect(self_direction, line)
                        self.direction = (new_direction.x, new_direction.y)
                        if self.bounces > 0:
                            self.bounces -= 1
                        else:
                            self.destroy()
                        return
                    else:
                        other.take_damage(self.hp_damage, self.shield_damage)
                        self.destroy()

            previous_line_point = new_point


class Wall(GameObject):
    """Some basic walls and stuff."""

    def draw(self):
        """Draw self."""
        draw_poly(self.x, self.y, self.vertices, self.color, GL_LINE_LOOP)

    def update(self, delta_time):
        """Does any update logic. This basic function does nothing. Please override. """
        self.y -= delta_time * SCROLL_SPEED
