import pygame
import random
import math

class Asteroid:
    LARGE = 3
    MEDIUM = 2
    SMALL = 1

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.radius = self.size * 10
        self.color = (150, 150, 150)  # Cinza para o asteroide
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.speed = 2 / self.size
        self.angle = random.uniform(0, 360)  # Ângulo de movimento aleatório

    def update(self):
        # Atualiza a posição do asteroide
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

        # Verificar bordas da tela e reaparecer do outro lado
        if self.x < 0:
            self.x = 800
        elif self.x > 800:
            self.x = 0
        if self.y < 0:
            self.y = 600
        elif self.y > 600:
            self.y = 0

        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    @staticmethod
    def create_split_asteroids(x, y, size):
        new_asteroids = []
        if size == Asteroid.LARGE:
            for _ in range(2):
                angle = random.uniform(0, 360)
                new_asteroid = Asteroid(x, y, Asteroid.MEDIUM)
                new_asteroid.angle = angle
                new_asteroids.append(new_asteroid)
        elif size == Asteroid.MEDIUM:
            for _ in range(3):
                angle = random.uniform(0, 360)
                new_asteroid = Asteroid(x, y, Asteroid.SMALL)
                new_asteroid.angle = angle
                new_asteroids.append(new_asteroid)
        return new_asteroids