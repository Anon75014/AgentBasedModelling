#%%
import sys

import numpy as np
import tianshou as ts
from gym import Env
from gym.spaces import Box, Dict, Discrete, Tuple

from crops import CropSortiment
from model import CropwarModel


class CropwarEnv(Env):
    def __init__(self) -> None:
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
            "water_levels": [0, 0, 3],
            "n_farmers": 4,
            # "v0_pos" : None,
            "v0_pos": [
                (5, 4),
                (5, 1),
                (1, 1),
                (1, 4),
            ],  # number of start positions must match n_farmers
            "start_budget": 50000000,
            "t_end": 50,  # Amount of time steps to be simulated
            "diagonal expansion": False,  # Only expand along the owned edges. like + and not x
            "save_gif": False,  # Save the map each timestep and generate Gif in the end
            "seed": 0,  # Use a new seed
            # "seed" : b'\xad\x16\xf3\xa7\x116\x10\x05\xc7\x1f'      # Use a custom seed
            # ML Variables:
            "nr_ml_farmers": 1,
        }

        # Create the model
        self.model = CropwarModel(self.parameters)

        """Setup for RL"""
        nr_stock_entries = self.parameters["amount_of_crops"]
        self.action_space = Dict(
            {
                "farm": Discrete(2),
                "sell": Box(low=0.0, high=100.0, dtype=np.float32, shape=(1,)),
            }
        )
        self.observation_space = Dict(
            {
                "budget": Box(low=0, high=np.inf, shape=(1,)),
                "stock": Box(low=0, high=np.inf, shape=(nr_stock_entries,)),
            }
        )

        print("Done: Initialised Environment.")

    def _reset_Cropshop(self):
        """Reset the CropShop used in the CropWar Model"""
        self.crop_shop = CropSortiment()
        self.crop_shop.add_crop(1, 1, 1)  # area, crop_type, available water
        self.crop_shop.add_crop(1, 9, 1)

    def step(self, action):
        reward = 0
        done = False

        info = {}
        return self.state, reward, done, info

    def render(self):
        pass

    def reset(self):
        self._reset_Cropshop()
        self.model = CropwarModel(self.parameters)
        print("Reset: CropShop & Model.")


env = CropwarEnv()
print(env.observation_space.sample())
print(env.action_space.sample())

# %%
