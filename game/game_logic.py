from game.game_objects.spaceship import Spaceship
from game.game_objects.asteroid import Asteroid
from game.level_manager import LevelManager
import pygame

class GameLogic:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spaceship = Spaceship(400, 300, self.screen_width, self.screen_height)
        self.level_manager = LevelManager()
        self.asteroids = self.level_manager.next_level((self.spaceship.x, self.spaceship.y))
        self.bullets = []
        self.lives = 3
        self.score = 0

    def handle_input(self, keys, current_frame):
        if keys[pygame.K_LEFT]:
            self.spaceship.rotate_left()
        if keys[pygame.K_RIGHT]:
            self.spaceship.rotate_right()
        if keys[pygame.K_UP]:
            self.spaceship.accelerate()
        if keys[pygame.K_DOWN]:
            self.spaceship.decelerate()
        if keys[pygame.K_SPACE]:
            self.spaceship.shoot(current_frame)

    def handle_action(self, action, current_frame):
        if action == 0:  # Rotate left
            self.spaceship.rotate_left()
        elif action == 1:  # Rotate right
            self.spaceship.rotate_right()
        elif action == 2:  # Accelerate
            self.spaceship.accelerate()
        elif action == 3:  # Decelerate
            self.spaceship.decelerate()
        elif action == 4:  # Shoot
            self.spaceship.shoot(current_frame)

    def update(self):
        self.spaceship.update()
        for bullet in self.bullets:
            bullet.update()
        for asteroid in self.asteroids:
            asteroid.update()
        episode_done, _ = self.check_collisions()
        self.check_level_completion()
        return episode_done

    def check_collisions(self):
        episode_done = False
        hit = False
        for asteroid in self.asteroids:
            if self.spaceship.rect.colliderect(asteroid.rect):
                self.lives -= 1
                self.asteroids.remove(asteroid)
                self.asteroids.extend(Asteroid.create_split_asteroids(asteroid.x, asteroid.y, asteroid.size))
                if self.lives <= 0:
                    episode_done = True

        for bullet in self.spaceship.bullets:
            for asteroid in self.asteroids:
                if bullet.rect.colliderect(asteroid.rect):
                    self.score += 1
                    self.spaceship.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    self.asteroids.extend(Asteroid.create_split_asteroids(asteroid.x, asteroid.y, asteroid.size))
                    hit = True
                    break
        return episode_done, hit

    def check_level_completion(self):
        if not self.asteroids:
            self.asteroids = self.level_manager.next_level((self.spaceship.x, self.spaceship.y))

    def render(self, screen):
        self.spaceship.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)

    def reset(self):
        self.spaceship = Spaceship(400, 300, self.screen_width, self.screen_height)
        self.level_manager = LevelManager()
        self.asteroids = self.level_manager.next_level((self.spaceship.x, self.spaceship.y))
        self.bullets = []
        self.lives = 3
        self.score = 0
