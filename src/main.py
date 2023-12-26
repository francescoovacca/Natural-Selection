import numpy as np
from dataclasses import dataclass

from Agent import AgentFeatures, BaseAgent
from Environment import Environment, EnvironmentFeatures


# different type of agents (not used atm)
@dataclass
class SetUp:
    is_cannibal: bool = False
    is_energetic: bool = True
    is_growing: bool = False
    is_faster: bool = False


class Day:

    def __init__(self, env: Environment):
        self.env = env

    def _agent_move(self, agent: BaseAgent):
        agent.move(self.env.env_features.grid_size)

    def _agent_eat(self, agent: BaseAgent):
        for food in self.env.food:
            distance = np.linalg.norm(np.array(agent.current_position) - np.array(food.current_position))
            if distance < self.env.env_features.eating_threshold and not food.is_eaten:
                agent.eat(food)
        self.env.food = [food for food in self.env.food if not food.is_eaten]

    def day_loop(self, show_viz=False):
        done = False
        while not done:  # go on until env is over
            for agent in self.env.agents:
                self._agent_move(agent)
                self._agent_eat(agent)
            done = self.env.day_is_over()

            # show environment after agent moves
            if show_viz:
                self.env.visualize()
        self.env.update()


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
    day = Day(env)
    agents_per_day = {}
    for n in range(n_days):
        if verbose:
            print(f"day {n}")
        agents_per_day[n] = env.agents
        day.day_loop()
    return env, agents_per_day


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
        sense=1.0
    )

    n_days = 30
    main(env_features, agent_features, n_days)
