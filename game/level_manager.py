from game.game_objects.asteroid import Asteroid
import random
import math

class LevelManager:
    def __init__(self):
        self.current_level = 0

    def next_level(self, spaceship_position):
        self.current_level += 1
        return self.generate_asteroids(spaceship_position)

    def generate_asteroids(self, spaceship_position):
        asteroids = []
        num_large = (self.current_level + 1) // 2
        num_medium = (self.current_level + 1) % 2 + self.current_level // 2

        for _ in range(num_large):
            x, y = self.random_position(spaceship_position)
            asteroids.append(Asteroid(x, y, Asteroid.LARGE))

        for _ in range(num_medium):
            x, y = self.random_position(spaceship_position)
            asteroids.append(Asteroid(x, y, Asteroid.MEDIUM))

        return asteroids

    def random_position(self, spaceship_position):
        safe_distance = 100
        while True:
            x, y = random.randint(0, 800), random.randint(0, 600)
            if math.sqrt((x - spaceship_position[0]) ** 2 + (y - spaceship_position[1]) ** 2) > safe_distance:
                return x, y