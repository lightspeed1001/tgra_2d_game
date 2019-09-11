import pygame
from pygame.locals import *
# from OpenGL.GL import *
# from OpenGL.GLU import *
from game_object_container import *
# import constants
from game_object import *
from level_loader import load_level
import sys
from random import random
from math import sqrt


class ShooterGame:
    def __init__(self):
        """Initializes game data."""
        # Player starts at the center
        player = Player(WINDOW_WIDTH // 2, 25, PLAYER_VERTICES, COLOR_PLAYER, 1, 1, 1)
        self.object_container = GameObjectContainer(player)
        self.clock = pygame.time.Clock()
        # TODO Make level into an array of levels, and once the player finishes a level, move to the next one
        self.level = load_level("level1")  # Maye sometime later, add more levels
        self.timer = 0
        pygame.display.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption('Shitty Shooting Game')
        glClearColor(0.0, 0.0, 0.0, 1.0)

        for obstacle in self.level:
            if obstacle["type"] == OBSTACLE_WALL:
                new_wall = Wall(400, 0, obstacle["data"], COLOR_WALL)
                self.object_container.walls.append(new_wall)
            elif obstacle["type"] == OBSTACLE_ENEMY:
                x, y = obstacle["data"]
                new_enemy = Enemy(x, y, ENEMY_VERTICES, COLOR_ENEMY, 2, 2)
                self.object_container.enemies.append(new_enemy)
                # self.object_container.enemies.append(obstacle["data"])

        self.clock.tick()

    def game_loop(self):
        """The main game loop. Takes care of updating, drawing, etc."""
        delta_time = self.clock.tick() / 1000  # tick is in ms, I want it in seconds
        for event in pygame.event.get():
            if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.exit_game()
            # Shooting logic is here, just because I want the player to only fire once per frame and making some
            # extra logic to facilitate that sounds like hassle.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # TODO Make powerups? Shoot directional bullets as well?
                bank_left = rotate_vector(BULLET_UP, 20)
                bank_right = rotate_vector(BULLET_UP, -20)
                self.object_container.bullets.append(self.object_container.player.shoot(BULLET_UP))
                self.object_container.bullets.append(self.object_container.player.shoot(bank_left))
                self.object_container.bullets.append(self.object_container.player.shoot(bank_right))

        pressed_keys = pygame.key.get_pressed()
        self.handle_input(pressed_keys, delta_time)

        self.update(delta_time)
        self.draw()

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def handle_input(self, pressed_keys, delta_time):
        """Handles any input required for moving the player."""
        if pressed_keys[pygame.K_LEFT]:
            self.object_container.player.move(PLAYER_LEFT, delta_time)
        if pressed_keys[pygame.K_RIGHT]:
            self.object_container.player.move(PLAYER_RIGHT, delta_time)
        if pressed_keys[pygame.K_UP]:
            self.object_container.player.move(PLAYER_UP, delta_time)
        if pressed_keys[pygame.K_DOWN]:
            self.object_container.player.move(PLAYER_DOWN, delta_time)
        self.restrain_player()

    def restrain_player(self):
        self.object_container.player.x = min(WINDOW_WIDTH, max(0, self.object_container.player.x))
        self.object_container.player.y = min(WINDOW_HEIGHT, max(0, self.object_container.player.y))

    def draw(self):
        """Draws all the objects on screen."""
        # Teacher boilerplate
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT)

        for obj in self.object_container.get_all_objects():
            obj.draw()

        pygame.display.flip()

    def update(self, delta_time):
        """Updates all the objects."""
        if self.object_container.player.hp <= 0:
            pass
            # self.exit_game()
            # return
        # Bullet collisions
        for bullet in self. object_container.bullets:
            for wall in self.object_container.walls:
                bullet.collision_check(wall, delta_time)
            bullet.collision_check(self.object_container.player, delta_time)
            for enemy in self.object_container.enemies:
                bullet.collision_check(enemy, delta_time)

        # Is an enemy supposed to fire?
        for enemy in self.object_container.enemies:
            if WINDOW_HEIGHT < enemy.y or enemy.y < 0:
                continue
            # No real logic here, just randomly shoot.
            if random() > 0.94:
                p_x, p_y = self.object_container.player.x, self.object_container.player.y
                direction_x = p_x - enemy.x
                direction_y = p_y - enemy.y
                direction_len = sqrt(direction_x ** 2 + direction_y ** 2)

                # TODO Player can't go inside enemies or walls
                if direction_len == 0:
                    continue
                direction = ((direction_x / direction_len) * BULLET_SPEED, (direction_y / direction_len) * BULLET_SPEED)

                # print("firing at {}".format(direction))
                self.object_container.bullets.append(enemy.shoot(direction))

        # Update loop and cleanup
        for obj in self.object_container.get_all_objects():
            obj.update(delta_time)
            if not obj.alive:
                self.object_container.delete_object(obj)

    def run(self):
        """Runs the game forever-ish."""
        while True:
            self.game_loop()


if __name__ == "__main__":
    game = ShooterGame()
    game.run()
