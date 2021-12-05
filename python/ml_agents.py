""" This file contains the specific, different ML Farmers. """
from typing import Dict

import numpy as np
from gym import spaces

from agents_base import BaseFarmer
from helper_functions import DotDict


class ML_Stationary(BaseFarmer):
    """Machine learning Introvert Farmer class.

    This Personality is based on the idea that, ...
    """

    data = DotDict(
        {
            "action_space": lambda nr_crops: spaces.MultiDiscrete([11, nr_crops]),
            "obs_dim": lambda *x: sum(x),
        }
    )

    planned_action = [None, None]

    def personality_traits(self):
        self.ACTIVE_TRAINING = False
        self.total_reward = 0

        self.buy_cell_threash = 1
        self.c_agent = {}
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
        price_array /= self.model.market.max_price
        budget_array /= self.p.max_budget

        state = np.concatenate(
            [stock_array, price_array, budget_array], dtype=np.float32
        )

        return state, bool(not self.model.running)

    def pre_market_step(self):
        """Used to step the agent: eg. do the following: harvest -> define their supply"""
        self.harvest()

        if not self.ACTIVE_TRAINING:
            state, _ = self.get_state()
            self.planned_action, _ = self.model.p.use_trained_model.predict(
                state, deterministic=True
            )

    def post_market_step(self):
        """Do the following: -> expand to random direction if the
        uniform probability sample is above the farmers buy_theshold.
        """
        # Introvert: Diese Personality expandiert nicht!
        self.change_to_crop(self.planned_action[1])

    def update(self):
        """Update base class and calculate reward."""
        super().update()

        # Measure Reward
        self.total_reward += self.rewarder()

    def rewarder(self) -> float:
        """Calculate Reward for this ML Farmers

        :return: ranking**2
        :rtype: float
        """
        reward = 0
        # Idea: The farmer gets max reward if richest. Then quadratically less for lower places
        # Info: if he has same budget as smb else, he is given the lower place reward
        ranking = np.where(self.model.sorted_budgets == self.budget)[0][0] / (
            self.model.p.n_farmers - 1
        )
        # print(ranking)  # for debug
        reward = ranking ** 2
        return reward


class ML_Expander(BaseFarmer):
    """Machine learning Introvert Farmer class.

    This Personality is based on the idea that, ...
    """

    data = DotDict(
        {
            "action_space": lambda nr_crops: spaces.MultiDiscrete(
                ([11] * nr_crops) + [nr_crops, 2]
            ),
            "obs_dim": lambda *x: sum(x),
        }
    )

    planned_action = [None, None]

    def personality_traits(self):
        self.ACTIVE_TRAINING = False
        self.total_reward = 0
        self.switch_action_index = self.model.p.amount_of_crops
        self.expand_action_index = self.model.p.amount_of_crops + 1

        self.buy_cell_threash = 1
        self.c_agent = {}
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
            supplies[crop_id] = (self.planned_action[crop_id] / 10) * self._stock[
                crop_id
            ]

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
        price_array /= self.model.market.max_price
        budget_array /= self.p.max_budget

        state = np.concatenate(
            [stock_array, price_array, budget_array], dtype=np.float32
        )

        return state, bool(not self.model.running)

    def pre_market_step(self):
        """Used to step the agent: eg. do the following: harvest -> define their supply"""
        self.harvest()

        if not self.ACTIVE_TRAINING:
            state, _ = self.get_state()
            self.planned_action, _ = self.model.p.use_trained_model.predict(
                state, deterministic=True
            )

    def post_market_step(self):
        """Do the following: -> expand to random direction if the
        uniform probability sample is above the farmers buy_theshold.
        """
        # Introvert: Diese Personality expandiert nicht!
        # Introvert: Diese Personality wechselt VIELLEICHT crop!

        if self.planned_action[self.expand_action_index]:
            # print("Im expanding =)")
            dir = self.random.choice(self.model.headings)
            self.find_and_buy(1, dir)
            self.change_to_crop(self.crop._id)
        self.change_to_crop(self.planned_action[self.switch_action_index])

    def update(self):
        """Update base class and calculate reward."""
        super().update()

        # Measure Reward
        self.total_reward += self.rewarder()

    def rewarder(self) -> float:
        """Calculate Reward for this ML Farmers

        :return: ranking**2
        :rtype: float
        """
        reward = 0
        # Idea: The farmer gets max reward if richest. Then quadratically less for lower places
        # Info: if he has same budget as smb else, he is given the lower place reward
        ranking = np.where(self.model.sorted_budgets == self.budget)[0][0] / (
            self.model.p.n_farmers - 1
        )
        total_budget = sum(self.model.sorted_budgets)
        budget_ranking = self.budget / total_budget
        # print(ranking)  # for debug

        total_supply = sum(
            [
                self.model.market.current_supply[crop_id]
                for crop_id in self.model.crop_shop.crops.keys()
            ]
        )
        supply = sum(
            [self.supply[crop_id] for crop_id in self.model.crop_shop.crops.keys()]
        )
        supply_ranking = supply / total_supply if total_supply != 0.0 else 0.0
        reward = (budget_ranking ** 2.0 + ranking ** 2.0 + supply_ranking ** 2) / 3.0
        return reward
