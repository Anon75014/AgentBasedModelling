#%%
import time
from copy import deepcopy

import gym
import numpy as np
from gym import spaces
from stable_baselines3.common.env_checker import check_env

from agents import *
from crops import *
from graph_presenter import graph_class
from map_presenter import map_class
from ml_agents import *
from model import CropwarModel
from settings import experiment_settings


class CropwarEnv(gym.Env):
    """Environment needed for RL training.

    This environment is basically a wrapper for the AgentPy model
    s.t. the SB3 training code can interact with the agent's environment.
    """

    def __init__(self) -> None:
        """initialisation"""
        super().__init__()

        """Setup of Model"""
        self._reset_Cropshop()

        self.p = experiment_settings["ML_Introvert_vs_3_Trader"]["base_parameters"]
        self.p.update(
            {
                # FIXED for the ML Environment:
                "crop_shop": self.crop_shop,
                "amount_of_crops": self.crop_shop.amount_of_crops,
                "ml_env": self,
                "trainee_type": ML_Expander,
                "farmers": {Trader: 3, Introvert: 0, ML_Stationary: 0, ML_Expander: 1},
                "seed": 0,
            }
        )

        self.p = DotDict(self.p)

        """ Infer Machine Learning Base-Personalty """

        print(f"Info: The active ML model is of type {self.p.trainee_type.__name__}")

        """Setup for RL"""
        nr_stock_entries = self.p.amount_of_crops
        nr_seeds = nr_stock_entries
        nr_farmers = sum(self.p.farmers.values())
        self.trainee_type = self.p.trainee_type

        self.observation_space = spaces.Box(
            0.0,
            1.0,
            shape=(
                self.trainee_type.data.obs_dim(nr_stock_entries, nr_seeds, nr_farmers),
            ),
            dtype=np.float32,
        )
        self.action_space = self.trainee_type.data.action_space(nr_stock_entries)

    def step(self, action: np.array):
        """Use action to step the environment.

        The "action" gets applied to the environment and a reward is calculated.

        :param action: an array containing the desired actions of the ML policy
        :type action: np.array
        :return: state, reward, done, info
        :rtype: np.array ; int ; bool ; dict
        """
        # Check if the received action is valid
        err_msg = f"{action!r} ({type(action)}) invalid"
        assert self.action_space.contains(action), err_msg

        """Steps and Updates"""
        self.ml_trainee.planned_action = action

        self.model.sim_step()

        """Evaluate the Action"""
        state, done = self.ml_trainee.get_state()
        reward = self.ml_trainee.rewarder()

        if (state > 1).any():
            print(state > 1)
            # Ensure normailsed observation-states:
            print("LIMIT REACHED. Training episode STOPS.")
            done = True

        if self.model.running == False:
            # Reached end of simulation
            done = True

        info = {}
        return state, reward, done, info

    def render(self, mode="human"):
        """Used for displaying the training.

        :param mode: for distinction of current mode, defaults to "human"
        :type mode: str, optional
        """
        pass

    def reset(self) -> np.array:
        """Resets the environment to the initial state.

        This way the agent can train again.

        :return: copy of the new state
        :rtype: np.array
        """
        self._reset_Cropshop()

        """ Initialise the model"""
        self.model = CropwarModel(dict(self.p))
        self.model.sim_setup()

        state, _ = self.ml_trainee.get_state()

        return state

    def seed(self, seed):
        """[summary]

        :param seed: [description]
        :type seed: [type]
        """
        pass

    def _reset_Cropshop(self):
        """Reset the CropShop used in the CropWar Model"""
        self.crop_shop = CropSortiment()
        self.crop_shop.add_crop(WinterWheat)
        self.crop_shop.add_crop(Barley)
        self.crop_shop.add_crop(Maize)
        self.crop_shop.add_crop(Beans)


def show_results(_model):
    env.model.end()
    env.model.create_output()
    env.model.output.info["completed"] = True
    env.model.output.info["created_objects"] = env.model._id_counter
    env.model.output.info["completed_steps"] = env.model.t
    env.model.output.info["run_time"] = "007"
    results = env.model.output
    print(results)
    presenter = graph_class(_model, results)

    presenter.crops()
    presenter.cellcount()
    presenter.stocks()
    presenter.budget()
    presenter.export()
    # presenter.traits(model)
    presenter.personalities()

    print(f"SEED: {_model.p.seed}")

    """ Display the Map with the farmers """
    mapper = map_class(_model)
    mapper.initialise_farmers()
    mapper.place_farmers()
    mapper.show()


if __name__ == "__main__":
    """For specific Env tests execute this file"""
    env = CropwarEnv()
    print(env.observation_space.sample())
    print(env.action_space.sample())

    # It will check environment and output additional warnings if needed
    # check_env(env, warn=True)

    env = CropwarEnv()
    obs = env.reset()
    print(f"obs: {obs}")
    n_steps = 16
    total_reward = 0
    for _ in range(n_steps):
        # Random action
        action = env.action_space.sample()
        print(f"action: {action}")
        obs, reward, done, info = env.step(action)
        _reward = env.model.ml_trainee.rewarder()
        print(_reward)
        total_reward += _reward
        if done:
            break
            obs = env.reset()
    print("TOTAL rew", total_reward)
    show_results(env.model)
