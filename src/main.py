import numpy as np
from dataclasses import dataclass

from src.Agent import AgentFeatures, BaseAgent
from src.Environment import Environment, EnvironmentFeatures


# different type of agents (not used atm)
@dataclass
class SetUp:
    is_cannibal: bool = False
    is_energetic: bool = True
    is_growing: bool = False
    is_faster: bool = False


class DayLoop:

    def __init__(self, env: Environment):
        self.env = env

    def _agent_move(self, agent: BaseAgent):
        agent.move(self.env.grid_size)

    def _agent_eat(self, agent: BaseAgent):
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

    def _restart(self):
        survived_agents = [agent for agent in self.env.agents if not agent.is_dead]
        num_reproductions = len([agent for agent in survived_agents if agent.food_eaten >= 2])
        new_agents = []
        self.env.foods = []
        self.env.agents = []
        self.env.initialize()

    def main_loop(self, show_viz=False):
        done = False
        # go on until env is over
        while not done:

            for agent in self.env.agents:
                # agents move on grid
                self._agent_move(agent)
                # agents eat food
                self._agent_eat(agent)
                # update status: dead or alive
                agent.update_life_status()

            done = self.env.is_game_over()

            # show environment after agent moves
            if show_viz:
                self.env.visualize()

        self._update(verbose=False)
        self._restart()


def main(
    env_features: EnvironmentFeatures,
    agent_features: AgentFeatures,
    n_days: int = 5,
    verbose=False
):
    """Run the whole script.

    :param env_features: stores the hyperparameters of the environment
    :param agent_features: stores the hyperparameters of the agens
    :param n_days: amount of days for which agents live up to lack of resources
    :param verbose: print the number of days elapsed, if True

    :returns: array storing the amount of agents per day (note: we must change return value to study traits evolution)
    """
    env = Environment(agent_features, env_features)
    day = DayLoop(env)
    agents_per_day = np.zeros(n_days, dtype=int)
    for n in range(n_days):
        if verbose:
            print(f"day {n}")
        agents_per_day[n] = env.num_agents
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
