import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from game_object_container import *
from constants import *
from game_object import *
from level_loader import load_level
import sys


class ShooterGame:
    def __init__(self):
        """Initializes game data."""
        player = Player(WINDOW_WIDTH // 2, 25, PLAYER_VERTICES, COLOR_PLAYER, 1, 1, 1)
        self.object_container = GameObjectContainer(player)
        self.clock = pygame.time.Clock()
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
                new_enemy = Enemy(x, y, ENEMY_VERTICES, COLOR_ENEMY, 10, 10)
                self.object_container.enemies.append(new_enemy)
                # self.object_container.enemies.append(obstacle["data"])

        self.clock.tick()

    def game_loop(self):
        """The main game loop. Takes care of updating, drawing, etc."""
        delta_time = self.clock.tick() / 1000
        for event in pygame.event.get():
            if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.object_container.bullets.append(self.object_container.player.shoot())


        pressed_keys = pygame.key.get_pressed()
        self.handle_input(pressed_keys, delta_time)
        
        self.update(delta_time)
        self.draw()

    def handle_input(self, pressed_keys, delta_time):
        if pressed_keys[pygame.K_LEFT]:
            self.object_container.player.move(PLAYER_LEFT, delta_time)
        if pressed_keys[pygame.K_RIGHT]:
            self.object_container.player.move(PLAYER_RIGHT, delta_time)
        if pressed_keys[pygame.K_UP]:
            self.object_container.player.move(PLAYER_UP, delta_time)
        if pressed_keys[pygame.K_DOWN]:
            self.object_container.player.move(PLAYER_DOWN, delta_time)

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
        for obj in self.object_container.get_all_objects():
            obj.update(delta_time)

    def run(self):
        """Runs the game forever-ish."""
        while True:
            self.game_loop()


if __name__ == "__main__":
    game = ShooterGame()
    game.run()
