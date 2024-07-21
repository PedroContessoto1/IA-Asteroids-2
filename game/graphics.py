
import pygame

def load_image(path):
    return pygame.image.load(path)

def draw_image(screen, image, position, angle=0):
    rotated_image = pygame.transform.rotate(image, angle)
    rect = rotated_image.get_rect(center=position)
    screen.blit(rotated_image, rect.topleft)
