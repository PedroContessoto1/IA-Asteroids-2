import torch
from torch.utils.tensorboard import SummaryWriter
from ai.ai_agent import DQNAgent
from ai.ai_simulation import AISimulation
import pygame
import os

def train_agent(num_episodes=1000, update_every=10, save_every=50, model_dir='models'):
    writer = SummaryWriter()

    env = AISimulation()
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    agent = DQNAgent(state_dim, action_dim)
    #agent.load_model('models/checkpoint_950.pth')  # Caminho para o modelo salvo

    render_mode = False
    os.makedirs(model_dir, exist_ok=True)  # Cria o diretório para salvar os modelos

    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0
        steps = 0

        for t in range(4000):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SLASH:
                    render_mode = not render_mode

            action = agent.select_action(state)
            next_state, reward, done, info = env.step(action)
            agent.push_memory(state, action, reward, next_state, done)

            state = next_state
            total_reward += reward
            steps = t + 1

            if t % update_every == 0:
                agent.optimize_model()

            if info['lives'] <= 0:
                break

            if render_mode:
                env.render()

        agent.update_target_net()

        writer.add_scalar('Episode/Total Reward', total_reward, episode)
        writer.add_scalar('Episode/Steps', steps, episode)
        writer.add_scalar('Agent/Epsilon', agent.epsilon, episode)

        print(f"Episode {episode}, Total Reward: {total_reward}, Steps: {steps}, Epsilon: {agent.epsilon}")

        # Salva o modelo a cada 'save_every' episódios
        if episode % save_every == 0 or episode == num_episodes - 1:
            save_path = os.path.join(model_dir, f'checkpoint_{episode}.pth')
            agent.save_model(save_path)
            print(f"Model saved at episode {episode}")

    pygame.quit()
    writer.close()

if __name__ == "__main__":
    train_agent()
