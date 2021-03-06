""" This file contains the specific, different Farmer personalities. """
from typing import Dict

import numpy as np

from agents_base import BaseFarmer


class Introvert(BaseFarmer):
    """
    Introvert Farmer class.

    This personality class implements the baseline agent of the model. It does
    not expand and tries to sell a fixed amount of its stock in each iteration.
    """

    def personality_traits(self):
        """
        Initialise class characteristics.
        """
        self.ml_controlled = False

        self.c_agent = {}
        self.buy_cell_threash = 1
        self.crop_id_init = self.random.randint(0, len(self.model.crop_shop.crops) - 1)

    def calc_supply(self, prices: Dict[int, int]) -> Dict[int, int]:
        """
        Initialises the agents supply function. The introvert farmer supplies,
        independent of market prices, 20% of the current stock of a certain crop.

        :param prices: Dictionary with the global prices for each `crop_id`
        :type prices: Dict[int, int]
        :return: Dictionary with the amounts that the agent supplies
        :rtype: Dict[int, int]
        """
        supplies = dict.fromkeys(self.model.crop_shop.crops.keys())
        for crop_id in self.model.crop_shop.crops.keys():
            supplies[crop_id] = 0.2 * self._stock[crop_id]

        self.supply = supplies
        return supplies

    def pre_market_step(self):
        """
        The pre-market step executes agents actions before market inteactions
        take place. In this case the agents farm and stock their harvest.
        """
        self.harvest()

    def post_market_step(self):
        """
        The post-market step executes strategy dependent actions. The introvert
        farmer is a baseline agents and therefore does not act.
        """
        pass


class Trader(BaseFarmer):
    """
    Trader Farmer class.

    The trader simulates a basic market agents. This agents class reacts on
    market outcomes, i.e. prices, and chooses an action that may increase the
    profit in future iterations.
    """

    def personality_traits(self):
        """
        Initialise class characteristics.
        """
        self.ml_controlled = False

        self.c_agent = {
            k: self.model.p.farmer_price_elasticity * self.model.random.random()
            for k in self.model.crop_shop.crops
        }

        self.buy_cell_threash = self.random.uniform(0, 1)  # ALTERNATIVE
        self.can_change_crop = True
        self.crop_id_init = self.random.randint(0, len(self.model.crop_shop.crops) - 1)

    def calc_supply(self, prices: Dict[int, int]) -> Dict[int, int]:
        """
        Initialises the agents supply function. The trader supplies according
        to a linear supply function.

        :param prices: Dictionary with the global prices for each `crop_id`
        :type prices: Dict[int, int]
        :return: Dictionary with the amounts that the agent supplies
        :rtype: Dict[int, int]
        """
        for crop_id in self.model.crop_shop.crops.keys():
            self.supply[crop_id] = np.min(
                [
                    self.model.p.market_base_supply
                    * (1.0 + self.c_agent[crop_id] * prices[crop_id]),
                    self._stock[crop_id],
                ]
            )
        return self.supply

    def pre_market_step(self):
        """
        The pre-market step executes agents actions before market inteactions
        take place. In this case the agents farm and stock their harvest
        """
        self.harvest()

    def post_market_step(self):
        """
        The post-market step executes strategy dependent actions. The trader
        can choose to change to another crop if the expected profit is
        positive.
        """
        # Probabilistic expansion
        direction = self.random.choice(self.model.headings)
        prob = self.random.uniform(0, 1)
        if prob > self.buy_cell_threash:
            self.find_and_buy(1, direction)
            self.change_to_crop(self.crop._id)

        self.market = self.model.market  # Easier access to the market

        # Calculates the expected profit of a crop change for two randomly
        # chosen crops based on current market prices and executes the crop
        # changes if expected profit is positive
        for crop_id in self.random.choices(
            list(self.model.crop_shop.crops.keys()), k=2
        ):
            if crop_id != self.crop_id:
                cost_seed_change = (
                    len(self.aquired_land)
                    * self.model.crop_shop.crops[crop_id].seed_cost
                )
                expected_profit = (
                    self.market.current_demand[crop_id]
                    - self.market.current_stock[crop_id]
                ) * self.model.crop_shop.crops[crop_id].sell_price
                expected_profit_current = (
                    self.market.current_demand[self.crop_id]
                    - self.market.current_stock[self.crop_id]
                ) * self.model.crop_shop.crops[self.crop_id].sell_price
                if expected_profit > expected_profit_current:
                    self.change_to_crop(crop_id)
