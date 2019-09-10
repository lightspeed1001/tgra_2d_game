WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

PLAYER_SPEED = 250
ENEMY_SPEED = 90
SCROLL_SPEED = 100
BULLET_SPEED = 320

PLAYER_LEFT = (-PLAYER_SPEED, 0)
PLAYER_RIGHT = (PLAYER_SPEED, 0)
PLAYER_UP = (0, PLAYER_SPEED)
PLAYER_DOWN = (0, -PLAYER_SPEED)

BULLET_LEFT = (-BULLET_SPEED, 0)
BULLET_RIGHT = (BULLET_SPEED, 0)
BULLET_UP = (0, BULLET_SPEED)
BULLET_DOWN = (0, -BULLET_SPEED)

OBSTACLE_WALL = "w"
OBSTACLE_ENEMY = "e"

ENEMY_VERTICES = ((-7, -7), (7, -7), (-7, 7), (7, 7))
PLAYER_VERTICES = ((-12, 0), (12, 0), (0, 25))

COLOR_PLAYER = (0.9, 0.9, 0.9)
COLOR_WALL = (1.0, 0.0, 0.0)
COLOR_ENEMY = (0.9, 0.0, 0.9)
COLOR_BULLET = (0.0, 0.0, 1.0)
