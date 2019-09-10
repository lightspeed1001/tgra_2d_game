class GameObjectContainer:
    def __init__(self, player, enemies=[], bullets=[], walls=[]):
        self.enemies = enemies
        self.player = player
        self.bullets = bullets
        self.walls = walls

    def get_all_objects(self):
        return self.enemies + self.bullets + self.walls + [self.player]
