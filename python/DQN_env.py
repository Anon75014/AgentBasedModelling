#%%
from copy import deepcopy

import gym
import numpy as np
from gym import spaces

from crops import CropSortiment
from model import CropwarModel


class CropwarEnv(gym.Env):
    # --.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--
    reward_threshold = 9
    # --'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--

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
            "start_budget": 50000000,
            "t_end": 10,  # Amount of time steps to be simulated
            "diagonal expansion": False,  # Only expand along the owned edges. like + and not x
            "save_gif": False,  # Save the map each timestep and generate Gif in the end
            "seed": 0,  # Use a new seed
            # "seed" : b'\xad\x16\xf3\xa7\x116\x10\x05\xc7\x1f'      # Use a custom seed
            # --'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--
            # ML Variables:
            "nr_ml_farmers": 1,
        }

        """ Initialise the model"""
        self.model = CropwarModel(self.parameters)
        self.model.setup()

        """Setup for RL"""
        nr_stock_entries = self.parameters["amount_of_crops"]

        self.observation_space = spaces.Box(
            0.0, np.inf, shape=(nr_stock_entries + 1,), dtype=np.float32
        )
        self.action_space = spaces.Discrete(2)  # spaces.MultiDiscrete([2,2])

        # # a potential structure:
        # self.action_space = Dict(
        #     {
        #         "farm": Discrete(2),
        #         "sell": Discrete(2),
        #     }
        # )
        # self.observation_space = Dict(
        #     {
        #         "budget": Box(low=0, high=np.inf, shape=(1,)),
        #         "stock": Box(low=0, high=np.inf, shape=(nr_stock_entries,)),
        #     }
        # )

        # print("Done: Initialised Environment.")

    def _reset_Cropshop(self):
        """Reset the CropShop used in the CropWar Model"""
        self.crop_shop = CropSortiment()
        self.crop_shop.add_crop(1, 1, 1)  # area, crop_type, available water
        self.crop_shop.add_crop(1, 9, 1)

    def step(self, action):
        # Check if the received action is valid
        err_msg = f"{action!r} ({type(action)}) invalid"
        assert self.action_space.contains(action), err_msg

        """Steps and Updates"""
        self.model.step()
        self.model.ml_step(action)

        self.model.update()

        self.state, done = self.model.ml_get_state()
        # state, done = self.model.get_state() #TODO generalise env?!?

        """Reward Calculation"""
        reward = 0
        ml_farmer = self.model.ml_farmers[0]

        # --.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--
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

    def render(self):
        pass

    def reset(self):
        self._reset_Cropshop()
        self.model = CropwarModel(self.parameters)
        self.model.setup()
        self.model.update()
        state, done = self.model.ml_get_state()
        return deepcopy(state)

    def seed(self, seed):
        np.random.seed(seed)


if __name__ == "__main__":
    """For specific Env tests execute this file"""
    env = CropwarEnv()
    print(env.observation_space.sample())
    print(env.action_space.sample())

# %%
