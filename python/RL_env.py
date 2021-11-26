#%%
from copy import deepcopy

import gym
import numpy as np
from gym import spaces

from crops import CropSortiment
from model import CropwarModel

from stable_baselines3.common.env_checker import check_env


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

        # Setup: Choose parameters for CropWar Model
        self.parameters = {
            # FIXED:
            "crop_shop": self.crop_shop,
            "amount_of_crops": self.crop_shop.amount_of_crops,
            # TUNABLE:
            # --.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--
            "water_levels": [0, 0, 3],
            "n_farmers": 4,
            # "v0_pos" : None,
            "v0_pos": [
                (5, 4),
                (5, 1),
                (1, 1),
                (1, 4),
            ],  # number of start positions must match n_farmers
            "start_budget": 1000,
            "t_end": 2,  # Amount of time steps to be simulated
            "diagonal expansion": False,  # Only expand along the owned edges. like + and not x
            "save_gif": False,  # Save the map each timestep and generate Gif in the end
            "seed": 0,  # Use a new seed
            # "seed" : b'\xad\x16\xf3\xa7\x116\x10\x05\xc7\x1f'      # Use a custom seed
            # --'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--
            # ML Variables:
            "nr_ml_farmers": 1,
            "use_trained_model": False,
            "max_stock": 2000,
            "max_budget": 30000000000,
        }

        """ Initialise the model"""
        self.model = CropwarModel(self.parameters)
        self.model.setup()

        """Setup for RL"""
        nr_stock_entries = self.parameters["amount_of_crops"]
        nr_farmers = self.parameters["n_farmers"]

        self.observation_space = spaces.Box(
            0.0, 1.0, shape=(nr_stock_entries + nr_farmers,), dtype=np.float32
        )
        self.action_space = spaces.MultiDiscrete([2, 2])

    def _reset_Cropshop(self):
        """Reset the CropShop used in the CropWar Model"""
        self.crop_shop = CropSortiment()
        self.crop_shop.add_crop(1, 1, 1)  # area, crop_type, available water
        # self.crop_shop.add_crop(1, 9, 1)

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
        self.model.step()
        self.model.ml_step(action)

        self.model.update()

        self.state, done = self.model.ml_get_state()

        if (self.state > 1).any():
            print("LIMIT REACHED")
            done = True

        """Reward Calculation"""
        reward = 0
        ml_farmer = self.model.ml_farmers[0]

        # --.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--
        # Idea: The farmer gets max reward if richest. Then quadratically less for lower places
        _budgets = self.model.farmers.budget
        budgets = np.array(_budgets)
        budgets.sort()
        ranking = np.where(budgets == ml_farmer.budget)[0][-1] / (len(budgets) - 1)
        # print(ranking)
        reward = ranking ** 2
        # --'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--

        info = {}
        self.model.t += 1
        return deepcopy(self.state), reward, done, info

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
        self.model = CropwarModel(self.parameters)
        self.model.setup()
        self.model.update()
        state, done = self.model.ml_get_state()

        return deepcopy(state)

    def seed(self, seed):
        """[summary]

        :param seed: [description]
        :type seed: [type]
        """
        np.random.seed(seed)


if __name__ == "__main__":
    """For specific Env tests execute this file"""
    env = CropwarEnv()
    print(env.observation_space.sample())
    print(env.action_space.sample())

    # It will check environment and output additional warnings if needed
    check_env(env, warn=True)
# %%
