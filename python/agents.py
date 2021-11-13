import agentpy as ap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
import Crop_model as cm
from pandas import DataFrame as df
import numpy as np
import copy


class FarmerPersonality(ABC):
    """
    Abstract base class for the personalities of the farmers

    --> Each personality refers to a certain strategy interaction for the market or expansion (to be implemented).
    """

    @abstractmethod
    def sell(self) -> bool:
        """Sell something"""

    @abstractmethod
    def change_crop(
        self,
        highest_price_id: int,
        current_demand: Dict[int, int],
        current_supply: Dict[int, int],
    ) -> bool:
        """Change crop"""


class Farmer(ap.Agent):
    def setup(self):
        """Initiate agent attributes."""
        self.grid = self.model.grid
        self.random = self.model.random
        np.random.seed(1234)  # Find out how to do this cleanly
        self.c_agent = {
            k: np.random.random() for k in self.model.crop_shop.crops
        }  # TODO: find good values

        # Set start budget
        self.budget = self.p.start_budget
        # self.field_locations = np.zeros(shape=(2,1)) # list where subfield locations are stored

        # Set start crop
        self.crop = None
        self.crop_id = self.random.randint(
            0, len(self.model.crop_shop.crops) - 1
        )  # -1 since len is  >= 1 and crop id starts at 0
        self.choose_crop(self.crop_id, start=True)

        # Initialise Stock
        # create an array of fixed size, where each entry corresponds to the amount in _stock:
        self._stock = {}
        for crop_id in self.model.crop_shop.crops.keys():
            self._stock[crop_id] = 0

        # self._stock = np.zeros(self.model.crop_shop.amount_of_crops, dtype=int)
        self.stock = copy.deepcopy(self._stock)

    def change_crop(
        self,
        crop_id: int,
        current_demand: Dict[int, int],
        current_supply: Dict[int, int],
    ) -> bool:
        cost_seed_change = self.crop_shop[crop_id].seed_cost
        price = self.crop_shop.crops[crop_id].sell_price
        expected_profit = cost_seed_change + (current_demand - current_supply) * price
        print(expected_profit)

    def choose_crop(self,
            new_id: int,
            current_demand: Dict[int, int]=None,
            current_supply: Dict[int, int]=None,
            start: bool=False
        ) -> bool:
        if start or self.change_crop(new_id, current_demand, current_supply):
            self.crop_id = new_id
            self.crop = self.model.crop_shop.crops[new_id]
            self.budget -= self.crop.seed_cost
            print(
                f"Farmer {self.id} changed crop to {self.crop_id}. New Budget: {self.budget}"
            )

    def farm(self):
        self._stock[self.crop_id] += self.crop.harvest_yield
        print(f"Farmer {self.id} harvested. New Stock: {self._stock}")

    def supply(self, prices: Dict[int, int]) -> Dict[int, int]:
        """
        Supply to the market

        Parameters
        ----------
        prices: Dict[int, int]
            Dictionary with the global prices for each `crop_id`


        Returns
        -------
        supplies: Dict[int, int]
            Dictionary with the amounts that the agent supplies
        """
        supplies = dict.fromkeys(self.model.crop_shop.crops.keys())
        for crop_id in self.model.crop_shop.crops.keys():
            supplying: int = np.min(
                [int(self.c_agent[crop_id] * prices[crop_id]), self._stock[crop_id]]
            )
            supplies[crop_id] = supplying
            self.sell(
                crop_id, supplying
            )  # Is there a reason to keep supply and sell separate?
        return supplies

    def sell(self, crop_id: int, amount: int):
        if self._stock[crop_id] >= amount:
            self._stock[crop_id] -= amount
            self.budget += amount * self.crop.sell_price
            print(
                f"Farmer {self.id} Sold {amount} of crop {crop_id}. New Stock: {self._stock}. New Budget: {self.budget}"
            )
        else:
            print(
                f"Ups: Farmer {self.id} does not have enough in _stock for that deal."
            )

    def step(self):
        self.farm()

        # amount = self.random.randint(0, 5)
        # self.sell(self.crop_id, amount)
        self.stock = copy.deepcopy(self._stock)
        print(f"Updated farmer {self.id}")
