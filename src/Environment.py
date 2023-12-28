import numpy as np
from dataclasses import dataclass

from Agent import BaseAgent, AgentFeatures
from Food import Food
import matplotlib.pyplot as plt


@dataclass
class EnvironmentFeatures:
    grid_size: int
    num_agents: int
    num_foods: int


class Environment:
    """
    Environment for simulating agent-based ecosystem.
    """
    def __init__(
        self,
        agent_features: AgentFeatures,
        env_features: EnvironmentFeatures,
    ):
        self.agent_features = agent_features
        self.env_features = env_features
        self.food = [self.generate_food() for _ in range(self.env_features.num_foods)]
        self.agents = [self.generate_agent() for _ in range(self.env_features.num_agents)]

    def generate_food(self) -> Food:
        """
        Generate a food item at a random location on the grid.
        """
        x = np.random.uniform(0, self.env_features.grid_size)
        y = np.random.uniform(0, self.env_features.grid_size)
        return Food((x, y))

    def generate_agent(self, parent: BaseAgent = None) -> BaseAgent:
        """
        Generate a new agent either randomly or from a parent agent.
        """
        x, y = np.random.uniform(0, self.env_features.grid_size, size=2)
        # Position the agent on the grid edges randomly
        if np.random.random() > 0.5:
            x = 0 if np.random.random() > 0.5 else self.env_features.grid_size
        else:
            y = 0 if np.random.random() > 0.5 else self.env_features.grid_size

        return BaseAgent((x, y), self.agent_features, parent)

    def update(self):
        """
        Update the environment for a new day.
        """
        # Regenerate food
        self.food = [self.generate_food() for _ in range(self.env_features.num_foods)]
        # Update agents
        new_agents = []
        for agent in self.agents:
            if not agent.is_dead():
                # Check if agent can replicate
                if agent.food_eaten >= 2:
                    new_agents.append(self.generate_agent(parent=agent))
                agent.reset()
                new_agents.append(agent)

        self.agents = new_agents

    def day_is_over(self):  # game over when no more food is left
        game_over = (len(self.food) == 0 or len(self.agents) == 0)
        return game_over

    def visualize(self):
        fig, ax = plt.subplots()
        if self.food:
            food_x, food_y = zip(*[food.current_position for food in self.food])
        else:
            food_x, food_y = None, None
        ax.scatter(food_x, food_y, c='red', label='Food')
        agent_x, agent_y = zip(*[agent.current_position for agent in self.agents])
        agent_food_eaten = [agent.food_eaten for agent in self.agents]

        # Calculate dot sizes based on food eaten
        # You can adjust the scaling factor as needed
        dot_sizes = [(1 + food_eaten) * 30 for food_eaten in agent_food_eaten]

        # Scatter plot for agents with variable dot sizes
        ax.scatter(agent_x, agent_y, c='blue', label='Agents', s=dot_sizes)

        ax.set_xlim(0, self.env_features.grid_size)
        ax.set_ylim(0, self.env_features.grid_size)
        ax.set_xlabel('X-coordinate')
        ax.set_ylabel('Y-coordinate')
        ax.legend()
        plt.pause(0.1)
        plt.show()

    def __repr__(self):
        return f"Agents: {self.agents}, \nFood: {self.food}"
