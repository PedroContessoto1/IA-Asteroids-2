import pygame
from game.game_logic import GameLogic
from game.settings import Settings
import numpy as np
import math
class AISimulation:
    def __init__(self):
        self.settings = Settings()
        self.logic = GameLogic(self.settings.screen_size[0], self.settings.screen_size[1])
        self.current_frame = 0

        # Definindo os espaços de observação e ação
        self.observation_space = type('', (), {"shape": (21,)})  # Espaço de observação com 21 elementos
        self.action_space = type('', (), {
            "n": 6})  # Espaço de ação com 6 ações possíveis: [0: virar esquerda, 1: virar direita, 2: acelerar, 3: desacelerar, 4: atirar, 5: nada]

        # Inicializa a tela para renderização
        self.previous_lives = self.logic.lives
        pygame.init()
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption("Asteroids AI Training")
        self.clock = pygame.time.Clock()

    def reset(self):
        self.logic.reset()
        self.current_frame = 0
        self.previous_lives = self.logic.lives
        return self.get_state()

    def step(self, action):
        self.current_frame += 1
        self.logic.handle_action(action, self.current_frame)

        episode_done = self.logic.update()
        next_state = self.get_state()
        reward, done = self.get_reward_done()
        info = {'lives': self.logic.lives}
        return next_state, reward, done, info

    def get_state(self):
        spaceship = self.logic.spaceship
        state = [
            spaceship.x,
            spaceship.y,
            spaceship.angle,
            spaceship.speed_x,
            spaceship.speed_y
        ]

        # Calcular a distância entre a nave e cada asteroide
        asteroids = self.logic.asteroids
        distances = [(asteroid, np.linalg.norm([spaceship.x - asteroid.x, spaceship.y - asteroid.y])) for asteroid in asteroids]
        distances.sort(key=lambda x: x[1])

        # Adicionar os três asteroides mais próximos
        for asteroid, distance in distances[:3]:
            state.extend([spaceship.x - asteroid.x, spaceship.y - asteroid.y])

        # Se houver menos de três asteroides, preencher com zeros
        while len(state) < 11:  # Nave: 5 elementos, 3 asteroides: 2*3 = 6 elementos
            state.extend([0, 0])

        # Informações sobre os tiros
        bullets = self.logic.spaceship.bullets
        if bullets:
            closest_bullet = min(bullets, key=lambda bullet: np.linalg.norm([spaceship.x - bullet.x, spaceship.y - bullet.y]))
            bullet_speed_x = closest_bullet.speed * math.cos(math.radians(closest_bullet.angle))
            bullet_speed_y = closest_bullet.speed * math.sin(math.radians(closest_bullet.angle))
            state.extend([closest_bullet.x, closest_bullet.y, bullet_speed_x, bullet_speed_y])
        else:
            state.extend([0, 0, 0, 0])

        # Se houver menos de 21 elementos, preencher com zeros
        while len(state) < 21:
            state.append(0)

        return np.array(state)

    def get_reward_done(self):
        reward = 0
        done = False

        # Penalidade por perda de vida
        # if self.logic.lives < self.previous_lives:
        #     reward -= 2
        #     self.previous_lives = self.logic.livegits
        #
        # # Verifica se todos os asteroides foram destruídos
        # if not self.logic.asteroids:
        #     reward += 10
        #     done = True

        # Verifica se houve acertos nos asteroides e incrementa o reward conforme necessário
        episode_done = self.logic.check_collisions()
        if episode_done:
            reward += 1
            done = True

        return reward, done

    def render(self):
        self.screen.fill(self.settings.bg_color)
        self.logic.render(self.screen)
        pygame.display.flip()
        self.clock.tick(self.settings.fps)
