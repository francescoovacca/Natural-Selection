import numpy as np
from dataclasses import dataclass


@dataclass
class AgentFeatures:
    energy: float
    speed: float
    size: int
    sense: float = 1.0


class BaseAgent:
    def __init__(self, position: tuple, agent_features: AgentFeatures, parent):
        self.agent_features = agent_features
        self.initial_position = position
        self.current_position = position  # coordinates of agent on env grid
        self.food_eaten = 0  # amount of food items eaten
        self.energy = agent_features.energy
        self.parent = parent  # this is an instance of BaseAgent, or none for first rounders

        def adjust_trait(trait_value):
            adjustment = np.random.choice([0.9, 1, 1.1])
            return trait_value * adjustment

        if not self.parent:
            self.speed = agent_features.speed
            self.size = agent_features.size
            self.sense = agent_features.sense
        else:
            self.speed = adjust_trait(self.parent.speed)
            self.size = adjust_trait(self.parent.size)
            self.sense = adjust_trait(self.parent.sense)

    def move(self, grid_size):
        # move randomly on x or y by step size
        step = self.speed if np.random.random() > 0.5 else - self.speed
        x, y = self.current_position
        if np.random.random() > 0.5:
            new_x = x
            new_y = (y + step) % grid_size
        else:
            new_x = (x + step) % grid_size
            new_y = y

        # update position
        self.current_position = new_x, new_y
        # remove energy consumed
        self.energy -= (self.size ** 3) * self.speed + self.sense

    def eat(self, food):
        # eat food and increase counter
        self.food_eaten += 1
        food.is_eaten = True

    def reset(self):
        self.food_eaten = 0
        self.energy = self.agent_features.energy
        self.current_position = self.initial_position

    def is_dead(self):
        is_dead = (self.food_eaten == 0) or (self.energy <= 0)
        return is_dead

    def __repr__(self):
        return f"position={self.current_position}, food_eaten={self.food_eaten}, energy={self.energy}\n"
