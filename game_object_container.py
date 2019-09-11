from game_object import *


class GameObjectContainer:
    """Responsible for keeping track of all the game objects."""
    def __init__(self, player, enemies=None, bullets=None, walls=None):
        if walls is None:
            walls = []
        if enemies is None:
            enemies = []
        if bullets is None:
            bullets = []

        self.enemies = enemies
        self.player = player
        self.bullets = bullets
        self.walls = walls

    def get_all_objects(self):
        return self.enemies + self.bullets + self.walls + [self.player]

    def delete_object(self, obj):
        if isinstance(obj, Bullet):
            self.bullets.remove(obj)
        elif isinstance(obj, Wall):
            self.walls.remove(obj)
        elif isinstance(obj, Enemy):
            self.enemies.remove(obj)
        elif isinstance(obj, Player):
            print("You died :(")
