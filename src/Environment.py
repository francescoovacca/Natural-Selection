import numpy as np
from dataclasses import dataclass

from src.Agent import BaseAgent, AgentFeatures
from src.Food import Food
import matplotlib.pyplot as plt


@dataclass
class EnvironmentFeatures:
    grid_size: int = 20
    num_agents: int = 10
    num_foods: int = 2
    eating_threshold: float = 1


class Environment:

    def __init__(self, agent_features: AgentFeatures, env_features: EnvironmentFeatures):
        self.agent_features = agent_features
        self.grid_size = env_features.grid_size
        self.num_foods = env_features.num_foods
        self.num_agents = env_features.num_agents
        self.eating_threshold = env_features.eating_threshold
        self.foods = []
        self.agents = []
        self.initialize()

    def add_food(self):  # add food on the grid randomly
        for _ in range(self.num_foods):
            x = np.random.uniform(0, self.grid_size)
            y = np.random.uniform(0, self.grid_size)
            food = Food((x, y))
            self.foods.append(food)

    def add_agents(self):  # add agents on the grid edges randomly
        for _ in range(self.num_agents):  # add as many agents as num_agents
            x, y = np.random.uniform(0, self.grid_size, size=2)
            if np.random.random() > 0.5:
                if np.random.random() > 0.5:
                    x = 0
                else:
                    x = self.grid_size
            else:
                if np.random.random() > 0.5:
                    y = 0
                else:
                    y = self.grid_size
            agent = BaseAgent((x, y), self.agent_features)
            self.agents.append(agent)

    def initialize(self):  # initialize grid with random food and agents
        self.add_food()
        self.add_agents()

    def is_game_over(self):  # game over when no more food is left
        game_over = (len(self.foods) == 0 or len(self.agents) <= 0)
        return game_over

    def visualize(self):
        fig, ax = plt.subplots()
        if self.foods:
            food_x, food_y = zip(*[food.position for food in self.foods])
        else:
            food_x, food_y = None, None
        ax.scatter(food_x, food_y, c='red', label='Food')
        agent_x, agent_y = zip(*[agent.position for agent in self.agents])
        agent_food_eaten = [agent.food_eaten for agent in self.agents]

        # Calculate dot sizes based on food eaten
        # You can adjust the scaling factor as needed
        dot_sizes = [(1 + food_eaten) * 30 for food_eaten in agent_food_eaten]

        # Scatter plot for agents with variable dot sizes
        ax.scatter(agent_x, agent_y, c='blue', label='Agents', s=dot_sizes)

        ax.set_xlim(0, self.grid_size)
        ax.set_ylim(0, self.grid_size)
        ax.set_xlabel('X-coordinate')
        ax.set_ylabel('Y-coordinate')
        ax.legend()
        plt.pause(0.1)
        plt.show()

    def __repr__(self):
        return f"Agents: {self.agents}, \nFood: {self.foods}"
