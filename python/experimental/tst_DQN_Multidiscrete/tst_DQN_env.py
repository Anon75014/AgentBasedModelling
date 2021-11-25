#%%
from copy import deepcopy
import random

import gym
import numpy as np
from gym import spaces

from tst_model import Ml_Model

# TODO implement seed function

class TestEnv(gym.Env):
    def __init__(self) -> None:

        """Setup of Model"""

        # Setup: Choose parameters for CropWar Model
        self.parameters = {
            "amount_of_crops" : 1,
            
            "start_budget": 0,
            "harvest_yield" : 10,
            "max_sell" : 15,
            
            "t_end": 10,  
            "seed": 0,  # Use a new seed

            # "seed" : b'\xad\x16\xf3\xa7\x116\x10\x05\xc7\x1f'      # Use a custom seed
        }

        # Create the model
        self.model = Ml_Model(self.parameters)
        self.model.setup()

        """Setup for RL"""
        nr_stock_entries = self.parameters["amount_of_crops"]

        self.observation_space = spaces.Box(0.0, np.inf, shape = (nr_stock_entries+1,), dtype=np.float32)
        # self.action_space = spaces.Discrete(2)
        self.action_space = spaces.Discrete(10)

        self.reward_threshold = 200000

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

        """Steps and Updates"""
        self.model.step(action)

        state, done = self.model.get_state()

        """Reward Calculation"""
        reward = 0
        if action: #[0]:
            self.action_counter += 1
            reward = (self.action_counter/self.model.p.t_end)**1.5
        
        if done:
            if self.model.stock == 0:
                reward += 10

        info = {}
        return state, reward, done, info

    def render(self):
        pass

    def reset(self):
        self.model.reset()
        self.action_counter = 0
        state, _ = self.model.get_state()
        return state

    def seed(self, seed):
        #self.model.p.seed(seed)
        print("Set seed NOT put in model")

if __name__ == "__main__":
    env = TestEnv()
    env.reset()
    print(f"state{env.model.get_state()}")
    print(env.observation_space.sample())
    print(env.action_space.sample())
    for i in range(30):
        act = random.randint(0,1)
        # act = np.array([random.randint(0,1),random.randint(0,1)])
        res = env.step(act)
        state, reward, done, info = res
        print(act,res)
        if done: 
            break
# %%