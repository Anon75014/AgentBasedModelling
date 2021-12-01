""" This file contains the specific, different Farmer personalities. """
from typing import Dict

import numpy as np

from agents_base import BaseFarmer


class Introvert(BaseFarmer):
    """Introvert Farmer class.

    This Personality is based on the idea that, ...
    """

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

        # Diese Personality schaut nicht auf den Markt!
        supplies = dict.fromkeys(self.model.crop_shop.crops.keys())
        for crop_id in self.model.crop_shop.crops.keys():
            supplies[crop_id] = 0.2 * self._stock[crop_id]

        self.supply = supplies
        return supplies

    def pre_market_step(self):
        """Used to step the agent: eg. do the following: harvest -> define their supply"""
        self.harvest()

    def post_market_step(self):
        """Do the following: -> expand to random direction if the
        uniform probability sample is above the farmers buy_theshold.
        """
        # Diese Personality expandiert nicht!
        # Diese Personality wechselt kein crop!


class Trader(BaseFarmer):
    """Trader Farmer class.

    This Personality is based on the idea that, ...
    """

    def personality_traits(self):
        """Distinctive personality traits of this farmer."""
        self.ml_controlled = False

        self.c_agent = {
            k: 0.001 * self.model.random.random() for k in self.model.crop_shop.crops
        }

        self.buy_cell_threash = self.random.uniform(0, 1) # ALTERNATIVE
        self.crop_id_init = self.random.randint(0, len(self.model.crop_shop.crops) - 1)

    def calc_supply(self, prices: Dict[int, int]) -> Dict[int, int]:
        """Calculates how much the farmer wants to supply

        :param prices: Dictionary with the global prices for each `crop_id`
        :type prices: Dict[int, int]
        :return: Dictionary with the amounts that the agent supplies
        :rtype: Dict[int, int]
        """
        # Diese Personality beobachtet und benutzt den Markt!
        supplies = dict.fromkeys(self.model.crop_shop.crops.keys())
        for crop_id in self.model.crop_shop.crops.keys():
            supplies[crop_id] = np.min(
                [self.c_agent[crop_id] * prices[crop_id], self._stock[crop_id]]
            )
        self.supply = supplies
        return supplies

    def pre_market_step(self):
        """Used to step the agent: eg. do the following: harvest -> define their supply"""
        self.harvest()

    def post_market_step(self):
        """Do the following: -> expand to random direction if the
        uniform probability sample is above the farmers buy_theshold.
        """


        dir = self.random.choice(self.model.headings)
        prob = self.random.uniform(0, 1)
        # Diese Personality expandiert (manchmal)!
        if prob > self.buy_cell_threash:
            self.find_and_buy(1, dir)
            self.change_to_crop(self.crop._id)

        # Diese Personality kann crop wechseln!
        
        self.market = self.model.market # get access to the CropWar market infos
        # potentially change crop:
        self.check_crop_change(
            # TODO CLEAN UP these references because highest price in market. no need to hand it to the check function
            self.market.highest_price_id,
            self.market.highest_price,
            self.market.current_demand[self.market.highest_price_id],
            self.market.current_supply[self.market.highest_price_id],
        )

    def check_crop_change(
                self,
                crop_id: int,
                price: int,
                current_demand: int,
                current_supply: int,
            ) -> None:
                """[summary]"""
                if crop_id != self.crop_id:
                    cost_seed_change = (
                        len(self.aquired_land)
                        * self.model.crop_shop.crops[crop_id].seed_cost
                    )
                    price = self.model.crop_shop.crops[crop_id].sell_price
                    expected_profit = (
                        cost_seed_change + (current_demand - current_supply) * price
                    )
                    print("Expected profit: ", expected_profit)
                    if expected_profit > 0:
                        self.change_to_crop(crop_id)


# %%
