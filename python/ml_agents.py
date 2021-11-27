""" This file contains the specific, different ML Farmers. """
from typing import Dict

import numpy as np

from agents_base import BaseFarmer
from helper_functions import DotDict
from gym import spaces


class ML_Introvert(BaseFarmer):
    """Machine learning Introvert Farmer class.

    This Personality is based on the idea that, ...
    """

    data = DotDict(
        {"action_space": spaces.MultiDiscrete([11]), "obs_dim": lambda *x: sum(x)}
    )

    planned_action = None

    def personality_traits(self):
        self.ml_controlled = False

        self.c_agent = {}
        self.buy_cell_threash = 1
        self.crop_id_init = self.random.randint(0, len(self.model.crop_shop.crops) - 1)

    def calc_supply(self, prices: Dict[int, int]) -> Dict[int, int]:
        """Calculates how much the farmer wants to supply

        :param prices: Dictionary with the global prices for each `crop_id`
        :type prices: Dict[int, int]
        :return: Dictionary with the amounts that the agent supplies
        :rtype: Dict[int, int]
        """
        
        # Diese ML Personality schaut b e s t i m m t auf den Markt! :D
        supplies = dict.fromkeys(self.model.crop_shop.crops.keys())
        for crop_id in self.model.crop_shop.crops.keys():
            supplies[crop_id] = (self.planned_action[0] / 10) * self._stock[crop_id]

        self.supply = supplies
        return supplies

    def get_state(self):
        """returns Environment state for ML.

        :return: state of env ; if done
        :rtype: np.array ; bool
        """
        """Get the Data"""
        stock_array = np.array(list(self._stock.values()), dtype=np.float32)
        price_array = np.array(
            [c.sell_price for c in self.model.crop_shop.crops.values()],
            dtype=np.float32,
        )
        budget_array = np.array(self.model.farmers.budget, dtype=np.float32)

        """Normalisation -> important for PPO algorithm"""
        stock_array /= self.p.max_stock
        price_array /= self.model.market.MAX_PRICE
        budget_array /= self.p.max_budget

        state = np.concatenate(
            [stock_array, price_array, budget_array], dtype=np.float32
        )

        return state, bool(self.model.running)

    def pre_market_step(self):
        """Used to step the agent: eg. do the following: harvest -> define their supply"""
        self.harvest()

    def post_market_step(self):
        """Do the following: -> expand to random direction if the
        uniform probability sample is above the farmers buy_theshold.
        """
        # Introvert: Diese Personality expandiert nicht!
        # Introvert: Diese Personality wechselt kein crop!
