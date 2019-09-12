from OpenGLWrapper import *
from constants import *
from math_stuff import *


class GameObject(object):
    """This is the base object for all the object in the game, such as enemies, player, etc."""

    def __init__(self, x, y, vertices, color):
        """Initialize the object"""
        # TODO Change self.x/y into Point, maybe vertices as well?
        # TODO Change self.direction into Vector.
        self.x = x
        self.y = y
        self.vertices = vertices
        self.color = color
        self.alive = True
        self.invulnerable = 0

    def __iter__(self):
        # To be able to iterate over lists of these easily
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
        # TODO Collision checks for things that aren't bullets
        # Could just treat the vertices as points and check those against other lines?
        # Don't have time. RIP
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

    def update(self, delta_time):
        if self.invulnerable > 0:
            self.invulnerable -= delta_time
            if self.color == COLOR_PLAYER:
                self.color = PLAYER_INVULN_COLOR
            else:
                self.color = COLOR_PLAYER
            if self.invulnerable <= 0:
                self.color = COLOR_PLAYER

    def shoot(self, direction):
        """Shoots a projectile straight."""
        new_bullet = PlayerBullet(self.x, self.y + 26, (0, 0), COLOR_BULLET, direction)
        return new_bullet

    def take_damage(self, hp_dmg, sh_dmg):
        """Take some damage."""
        if self.invulnerable > 0:
            return
        
        if self.shields <= 0:
            self.hp = max(0, self.hp - hp_dmg)
        else:
            self.shields = max(0, self.shields - sh_dmg)
        self.invulnerable = PLAYER_INVULN_TIME
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
        new_bullet = EnemyBullet(self.x, self.y - 16, (0, 0), COLOR_ENEMY_BULLET, direction)
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
        if self.shields <= 0:
            self.hp = max(0, self.hp - hp_dmg)
        else:
            self.shields = max(0, self.shields - sh_dmg)

        if self.shields <= 0:
            self.color = (0.8, 0.3, 0.3)
        if self.hp <= 0:
            self.die()
        


class Bullet(GameObject):
    """Basic bullet object."""

    def __init__(self, x, y, vertices, color, direction, hp_damage=1, shield_damage=1,
                 bounces=2, ttl=BULLET_TIME_TO_LIVE):
        super().__init__(x, y, vertices, color)
        self.direction = direction
        self.hp_damage = hp_damage
        self.shield_damage = shield_damage
        self.bounces = bounces
        self.ttl = ttl

    def draw(self):
        """Draw self."""
        draw_point(self.x, self.y, 5, self.color)

    def update(self, delta_time):
        self.x += self.direction[0] * delta_time
        self.y += self.direction[1] * delta_time
        self.ttl -= delta_time
        if self.ttl <= 0:
            self.destroy()

    def collision_check(self, other, delta_time):
        """Checks if the object collides with other."""
        # This is just a particle, so we can use the math_stuff thingy
        self_point = Point(self.x, self.y)
        self_direction = Vector(self.direction[0], self.direction[1])

        previous_line_point = other.vertices[0]
        previous_line_point = Point(other.x - previous_line_point[0], other.y + previous_line_point[1])

        for line_point in other.vertices[1:] + other.vertices[0:1]:
            new_point = Point(other.x - line_point[0], other.y + line_point[1])

            line = (previous_line_point, new_point)
            time_to_hit = t_hit(line, self_point, self_direction)
            if delta_time + DELTA_WIGGLE >= time_to_hit >= 0:
                where_hit = p_hit(self_point, time_to_hit, self_direction)
                # TODO Fix the collision detection sometimes letting things through
                x_dist = abs(new_point.x - previous_line_point.x)
                y_dist = abs(new_point.y - previous_line_point.y)
                collides = False
                if x_dist > y_dist:
                    if new_point.x <= where_hit.x <= previous_line_point.x or \
                        previous_line_point.x <= where_hit.x <= new_point.x:
                        collides = True
                else:
                    if new_point.y <= where_hit.y <= previous_line_point.y or \
                        previous_line_point.y <= where_hit.y <= new_point.y:
                        collides = True
                
                if collides:
                    if isinstance(other, Wall):
                        new_direction = reflect(self_direction, line)
                        self.direction = (new_direction.x, new_direction.y)
                        if self.bounces > 0:
                            self.bounces -= 1
                        else:
                            self.destroy()
                        return
                    else:
                        if isinstance(self, PlayerBullet) and not isinstance(other, Player) \
                                or isinstance(self, EnemyBullet) and not isinstance(other, Enemy):
                            other.take_damage(self.hp_damage, self.shield_damage)
                            self.destroy()
            previous_line_point = new_point


class PlayerBullet(Bullet):
    # Dummy class for now.
    pass


class EnemyBullet(Bullet):
    # Dummy class for now.
    pass


class Wall(GameObject):
    """Some basic walls and stuff."""

    def draw(self):
        """Draw self."""
        draw_poly(self.x, self.y, self.vertices, self.color, GL_LINE_LOOP)

    def update(self, delta_time):
        """Scrolls the obstacle down slowly."""
        self.y -= delta_time * SCROLL_SPEED
