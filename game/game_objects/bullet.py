import pygame
import math

class Bullet:
    def __init__(self, x, y, angle, screen_width, screen_height, speed=10, lifespan=50):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.radius = 3
        self.color = (255, 255, 255)  # Cor branca para o projétil
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.frames_alive = 0
        self.lifespan = lifespan

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))
        self.rect.center = (self.x, self.y)

        # Wrap around screen edges
        if self.x < 0:
            self.x = self.screen_width
        elif self.x > self.screen_width:
            self.x = 0
        if self.y < 0:
            self.y = self.screen_height
        elif self.y > self.screen_height:
            self.y = 0

        self.frames_alive += 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_expired(self):
        return self.frames_alive >= self.lifespan