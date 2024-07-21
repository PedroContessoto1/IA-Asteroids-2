import pygame
from game.game_logic import GameLogic
from game.settings import Settings


class GameEngine:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.logic = GameLogic(self.settings.screen_size[0], self.settings.screen_size[1])
        self.font = pygame.font.SysFont(None, 36)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            current_frame = pygame.time.get_ticks()
            self.logic.handle_input(keys, current_frame)
            self.logic.update()

            self.screen.fill(self.settings.bg_color)
            self.logic.render(self.screen)

            self.display_score_and_lives()

            pygame.display.flip()
            self.clock.tick(self.settings.fps)

        pygame.quit()

    def display_score_and_lives(self):
        score_text = self.font.render(f"Score: {self.logic.score}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {self.logic.lives}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))