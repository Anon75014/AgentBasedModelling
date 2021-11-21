#%%
from copy import deepcopy

import gym
import numpy as np
from gym import spaces
import tianshou as ts

from tst_model import TestModel

# TODO implement seed function

class TestEnv(gym.Env):
    def __init__(self) -> None:
        super().__init__()

        """Setup of Model"""

        # Setup: Choose parameters for CropWar Model
        self.parameters = {
            "amount_of_crops" : 1,
            "start_budget": 50000000,
            "t_end": 50,  # Amount of time steps to be simulated
            "seed": 0,  # Use a new seed
            # "seed" : b'\xad\x16\xf3\xa7\x116\x10\x05\xc7\x1f'      # Use a custom seed
        }

        # Create the model
        self.model = TestModel(self.parameters)
        self.model.setup()
        """Setup for RL"""
        nr_stock_entries = self.parameters["amount_of_crops"]
        self.observation_space = spaces.Box(0.0, np.inf, shape = (nr_stock_entries+1,), dtype=np.float32)
        # self.action_space = spaces.Discrete(2) 
        self.action_space = spaces.Discrete(2) # spaces.MultiBox([2,2])

        
        # self.action_space = Dict(
        #     {
        #         "farm": Discrete(2),
        #         "sell": Discrete(2), # Box(low=0.0, high=100.0, dtype=np.float32, shape=(1,)),
        #     }
        # )
        # self.observation_space = Dict(
        #     {
        #         "budget": Box(low=0, high=np.inf, shape=(1,)),
        #         "stock": Box(low=0, high=np.inf, shape=(nr_stock_entries,)),
        #     }
        # )

        # print("Done: Initialised TestEnvironment.")

    def step(self, action):
        err_msg = f"{action!r} ({type(action)}) invalid"
        assert self.action_space.contains(action), err_msg

        reward = 0
        done = False

        """Steps and Updates"""
        self.model.ml_step(action)

        state = self.model.ml_get_state()
        done : bool = self.model.at_last_step()

        """Reward Calculation"""
        # if action[0]:
        #     reward += 2
        if action:
            reward += 2

        if done:
            if self.model.budget >= 100: #max(self.farmers.budget):
                reward += 10

        info = {}

        return deepcopy(state), reward, done, info

    def render(self):
        pass

    def reset(self):
        self.model.reset()
        self.model.update()
        state = self.model.ml_get_state()
        # print("Reset: TestModel.")
        return deepcopy(state)

    def seed(self, seed):
        self.model.random.seed(seed)
        print("Set seed in model")

if __name__ == "__main__":
    env = TestEnv()
    print(env.model.ml_get_state())
    print(env.observation_space.sample())
    print(env.action_space.sample())

# %%