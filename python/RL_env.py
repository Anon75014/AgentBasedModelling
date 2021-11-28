#%%
from copy import deepcopy

import gym
import numpy as np
from gym import spaces
from stable_baselines3.common.env_checker import check_env

from agents import *
from ml_agents import *
from crops import CropSortiment
from model import CropwarModel


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

        self.parameters = {
            # FIXED:
            "crop_shop": self.crop_shop,
            "amount_of_crops": self.crop_shop.amount_of_crops,
            # TUNABLE:
            # --.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--
            "water_levels": [0, 0, 3],
            # "v0_pos" : None,
            "v0_pos": sorted(
                [
                    (1, 1),
                    (1, 4),
                    (5, 1),
                    (5, 4),
                ],
                key=lambda x: x[0],
            ),  # number of start positions must match n_farmers
            "start_budget": 1000,
            "t_end": 50,  # Amount of time steps to be simulated
            "diagonal expansion": False,  # Only expand along the owned edges. like + and not x
            "save_gif": False,  # Save the map each timestep and generate Gif in the end
            "seed": 0,  # Use a new seed
            # "seed" : b'\xad\x16\xf3\xa7\x116\x10\x05\xc7\x1f'      # Use a custom seed
            # --'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--
            "nr_ml_farmers": 1,
            "n_farmers": 4,
            "farmers": {Trader: 0, Introvert: 3, ML_Introvert: 1},
            "ml_env": self,
            "use_trained_model": False,
            "max_stock": 2000,
            "max_budget": 1e8,
            "river_content": 12.0,
            "market_base_demand": 10.0,
            "market_demand_fraction": 0.7,
        }

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
        self.action_space = self.ml_type.data.action_space

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

        self.model.step()

        state, done = self.ml_trainee.get_state()

        if (state > 1).any():
            # Ensure normailsed observation-states:
            print("LIMIT REACHED. Training episode STOPS.")
            done = True

        if self.model.running == False:
            # Reached end of simulation
            done = True
            
        """Reward Calculation"""
        reward = 0
        # --.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--
        # Idea: The farmer gets max reward if richest. Then quadratically less for lower places
        _budgets = self.model.farmers.budget
        budgets = np.array(_budgets)
        budgets.sort()
        ranking = np.where(budgets == self.ml_trainee.budget)[0][-1] / (
            len(budgets) - 1
        )
        # print(ranking)  # for debug
        reward = ranking ** 2
        # --'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--

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


if __name__ == "__main__":
    """For specific Env tests execute this file"""
    env = CropwarEnv()
    print(env.observation_space.sample())
    print(env.action_space.sample())

    # It will check environment and output additional warnings if needed
    check_env(env, warn=True)
# %%
