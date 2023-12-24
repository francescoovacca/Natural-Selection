import numpy as np
from dataclasses import dataclass

from Agent import AgentFeatures
from Environment import Environment, EnvironmentFeatures


# different type of agents (not used atm)
@dataclass
class SetUp:
    is_cannibal: bool = False
    is_energetic: bool = True
    is_growing: bool = False
    is_faster: bool = False


class DayLoop:

    def __init__(self, env):
        self.env = env

    def _agents_move(self, agent):
        agent.move(self.env.grid_size)

    def _agents_eat(self, agent):
        for food in self.env.foods:
            distance = np.linalg.norm(np.array(agent.position) - np.array(food.position))
            if distance < self.env.eating_threshold and not food.is_eaten:
                agent.eat(food)
        self.env.foods = [food for food in self.env.foods if not food.is_eaten]

    def _update(self, verbose=False):
        env = self.env
        num_agents_survived = len([agent for agent in env.agents if agent.food_eaten >= 1])
        num_agents_reproduced = len([agent for agent in env.agents if agent.food_eaten == 2])
        if verbose:
            print(f"agents survived = {num_agents_survived}")
            print(f"agents reproduced = {num_agents_reproduced}")
        env.num_agents = num_agents_survived + num_agents_reproduced

    def _restart(self):  # restart the grid (when game is over at the end of the day with new amount of agents)
        self.env.foods = []
        self.env.agents = []
        self.env.initialize()

    def main_loop(self, show_viz=False):
        env = self.env
        done = False
        while not done:  # go on until env is over
            for agent in env.agents:  # loop on all agents and let them move and eat
                self._agents_move(agent)
                self._agents_eat(agent)
            done = env.is_game_over()
            if show_viz:
                env.visualize()
        self._update(verbose=False)
        self._restart()


def main(
    env_features: EnvironmentFeatures,
    agent_features: AgentFeatures,
    n_days: int = 5
):
    """Run the whole script.

    :param env_features: stores the hyperparameters of the environment
    :param agent_features: stores the hyperparameters of the agens
    :param n_days: amount of days for which agents live up to lack of resources

    :returns: array storing the amount of agents per day (note: we must change return value to study traits evolution)
    """
    env = Environment(agent_features, env_features)
    day = DayLoop(env)
    agents_per_day = np.zeros(n_days, dtype=int)
    for i in range(n_days):
        agents_per_day[i] = env.num_agents
        day.main_loop()
    return agents_per_day


if __name__ == "__main__":
    env_features = EnvironmentFeatures(
        grid_size=10,
        num_agents=10,
        num_foods=5,
        eating_threshold=1,
    )

    agent_features = AgentFeatures(
        speed=1,  # agent will take a step of length 1 on the grid of size 10
        energy=np.inf,  # not using energy constraint
        size=100,  # not implemented yet but we'll have to
    )

    n_days = 30
    main(env_features, agent_features, n_days)
