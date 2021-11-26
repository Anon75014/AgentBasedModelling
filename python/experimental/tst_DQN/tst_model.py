""" This file contains the Main structure of the Simulation. -> The AgentPy model """

import os
from copy import deepcopy

import agentpy as ap
import numpy as np


class TestModel(ap.Model):
    """An Agent-Based-Model to simulate the crop war of farmers."""

    # See documentation https://agentpy.readthedocs.io/en/latest/reference_grid.html#agentpy.Grid
    def __init__(self, parameters) -> None:
        super().__init__(parameters)

    def setup(self):
        """Setting parameters and model properties"""
        # Setting random seed (for reproducibility)
        if self.p.seed == 0:
            self.p.seed = os.urandom(10)  # a random seed of length
        self.random.seed(self.p.seed)

        self.budget = self.p.start_budget
        self.stock = 0

    def reset(self):
        self.budget = self.p.start_budget
        self.stock = 0

    def harvest(self):
        self.stock += self.p.harvest_yield

    def sell(self, amount):
        price = 1

        if self.stock < amount:
            return 1

        self.budget += amount * price
        self.stock -= amount
        return 0

    def at_last_step(self) -> bool:
        return self.t == self.p.t_end

    def step(self):
        if self.t > self.p.t_end:  # model should stop after "t_end" steps
            # self.stop()
            print("REACHED THE END")
        else:
            print(f"\n    Start of time step: {self.t}")

    def update(self):
        pass

    def end(self):
        pass


class Ml_Model(TestModel):
    def __init__(self, parameters) -> None:
        super().__init__(parameters)
        self.setup()

    def step(self, action):
        """Applies the action decided by the DQN to the model
        Inputs:
            action : [Bool: Farm, Proportion: Sell of active crop \in [0,1]]
        """
        # if action[0]: #for multibox([2,2]) state
        #     self.harvest()
        self.harvest()

        if action:
            amount = min(self.stock, self.p.max_sell)
            self.sell(amount)

        self.t += 1
        return 0

    def get_state(self):
        time_up = False
        if self.t >= self.p.t_end:
            time_up = True
        state = deepcopy(np.array([self.budget, self.stock], dtype=np.float32))

        return state, int(time_up)


#%%
