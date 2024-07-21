import pygame
import math
from game.game_objects.bullet import Bullet

class Spaceship:
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed_x = 0
        self.speed_y = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.deceleration = 0.05
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.original_image = pygame.image.load("game/assets/spaceship.png")
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))  # Redimensionar a imagem da nave
        self.image = pygame.transform.rotate(self.original_image, -90)  # Girar a imagem 90 graus para a direita
        self.rect = self.image.get_rect(center=(x, y))
        self.bullets = []
        self.last_shot_frame = 0

    def update(self):
        # Atualiza a posição da nave com base na velocidade e no ângulo
        self.x += self.speed_x
        self.y += self.speed_y

        # Limitar a velocidade
        speed = math.sqrt(self.speed_x**2 + self.speed_y**2)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.speed_x *= scale
            self.speed_y *= scale

        # Verificar bordas da tela
        if self.x < 0:
            self.x = self.screen_width
        elif self.x > self.screen_width:
            self.x = 0
        if self.y < 0:
            self.y = self.screen_height
        elif self.y > self.screen_height:
            self.y = 0

        self.rect.center = (self.x, self.y)

        # Atualizar os projéteis
        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle - 90)  # Ajustar a rotação para a posição correta
        screen.blit(rotated_image, rotated_image.get_rect(center=self.rect.center).topleft)

        # Desenhar os projéteis
        for bullet in self.bullets:
            bullet.draw(screen)

    def rotate_left(self):
        self.angle += 5

    def rotate_right(self):
        self.angle -= 5

    def accelerate(self):
        # Acelera na direção atual da nave
        self.speed_x += self.acceleration * math.cos(math.radians(self.angle))
        self.speed_y -= self.acceleration * math.sin(math.radians(self.angle))

    def decelerate(self):
        # Desacelera a nave gradualmente
        self.speed_x *= (1 - self.deceleration)
        self.speed_y *= (1 - self.deceleration)
        if abs(self.speed_x) < 0.01:
            self.speed_x = 0
        if abs(self.speed_y) < 0.01:
            self.speed_y = 0
    def shoot(self, current_frame, frame_interval=300):
        if current_frame - self.last_shot_frame >= frame_interval:  # Verificar intervalo de frames
            bullet = Bullet(self.x, self.y, self.angle)
            self.bullets.append(bullet)
            self.last_shot_frame = current_frame
