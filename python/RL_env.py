#%%
import time
from copy import deepcopy

import gym
import numpy as np
from gym import spaces
from stable_baselines3.common.env_checker import check_env

from agents import *
from crops import CropSortiment
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
        # Initialise: CROPS
        self._reset_Cropshop()

        self.parameters = experiment_settings["Stationary_ML_vs_3_Trader"][
            "base_parameters"
        ]
        self.parameters.update(
            {
                # FIXED for the ML Environment:
                "crop_shop": self.crop_shop,
                "amount_of_crops": self.crop_shop.amount_of_crops,
                "ml_env": self,
            }
        )

        """ Infer Machine Learning Base-Personalty """
        self.ml_type = [
            k
            for k, v in self.parameters["farmers"].items()
            if k.__name__[:2] == "ML" and v > 0
        ][0]
        print(f"Info: The active ML model is of type {self.ml_type.__name__}")

        """Setup for RL"""
        nr_stock_entries = self.parameters["amount_of_crops"]
        nr_seeds = nr_stock_entries
        nr_farmers = self.parameters["n_farmers"]

        self.observation_space = spaces.Box(
            0.0,
            1.0,
            shape=(self.ml_type.data.obs_dim(nr_stock_entries, nr_seeds, nr_farmers),),
            dtype=np.float32,
        )
        self.action_space = self.ml_type.data.action_space(nr_stock_entries)

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

        state, done = self.ml_trainee.get_state()

        if (state > 1).any():
            # Ensure normailsed observation-states:
            print("LIMIT REACHED. Training episode STOPS.")
            # time.sleep(2)
            done = True

        if self.model.running == False:
            # Reached end of simulation
            # print("MODEL NOT running anymore ",self.model.t)
            # time.sleep(2)

            done = True

        """Reward Calculation"""
        reward = self.model.rewarder()
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
        self.model = CropwarModel(self.parameters)
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
        self.crop_shop.add_crop(1, 1, 1)  # area, crop_type, available water
        self.crop_shop.add_crop(1, 2, 1)  # area, crop_type, available water
        self.crop_shop.add_crop(1, 3, 1)  # area, crop_type, available water
        self.crop_shop.add_crop(1, 4, 1)  # area, crop_type, available water
        self.crop_shop.add_crop(1, 9, 1)


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
    check_env(env, warn=True)

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
        _reward = env.model.rewarder()
        print(_reward)
        total_reward += _reward
        if done:
            break
            obs = env.reset()
    print("TOTAL rew", total_reward)
    show_results(env.model)

# %%
