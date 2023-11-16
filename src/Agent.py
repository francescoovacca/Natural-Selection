import numpy as np
from dataclasses import dataclass


@dataclass
class AgentFeatures:
    speed: float
    energy: float
    size: int


class BaseAgent:
    def __init__(self, position: tuple, agent_features: AgentFeatures):
        self.position = position  # coordinates of agent on env grid
        self.food_eaten = 0  # amount of food items eaten
        self.is_dead = False  # can be alive or dead
        self.speed = agent_features.speed
        self.energy = agent_features.energy
        self.size = agent_features.size

    def move(self, grid_size):
        # move randomly on x or y by step size
        step = self.speed if np.random.random() > 0.5 else - self.speed
        x, y = self.position
        if np.random.random() > 0.5:
            new_x = x
            new_y = (y + step) % grid_size
        else:
            new_x = (x + step) % grid_size
            new_y = y
        self.position = new_x, new_y

    def eat(self, food):
        # eat food and increase counter
        self.food_eaten += 1
        food.is_eaten = True

    def __repr__(self):
        return f"position={self.position}, is_dead={self.is_dead}, food_eaten={self.food_eaten}\n"
