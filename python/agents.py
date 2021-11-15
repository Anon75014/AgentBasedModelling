import agentpy as ap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
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
        self.c_agent = {
            k: 0.001 * self.model.random.random() for k in self.model.crop_shop.crops
        }  # TODO: find good values

        # Set start budget
        self.budget = self.p.start_budget
        # self.field_locations = np.zeros(shape=(2,1)) # list where subfield locations are stored

        # Set start crop
        self.crop = None
        self.crop_id = self.random.randint(
            0, len(self.model.crop_shop.crops) - 1
        )  # -1 since len is  >= 1 and crop id starts at 0
        self.choose_crop(self.crop_id)

        # Initialise Stock
        # create an array of fixed size, where each entry corresponds to the amount in _stock:
        self._stock = {}
        for crop_id in self.model.crop_shop.crops.keys():
            self._stock[crop_id] = 0
        self.supply = dict.fromkeys(self.model.crop_shop.crops.keys())


        # self._stock = np.zeros(self.model.crop_shop.amount_of_crops, dtype=int)
        self.stock = copy.deepcopy(self._stock)

    def check_crop_change(
        self,
        crop_id: int,
        price: int,
        current_demand: int,
        current_supply: int,
    ) -> None:
        if crop_id != self.crop_id:
            cost_seed_change = self.model.crop_shop.crops[crop_id].seed_cost - self.model.crop_shop.crops[self.crop_id].seed_cost
            price = self.model.crop_shop.crops[crop_id].sell_price
            expected_profit = cost_seed_change + (current_demand - current_supply) * price
            print("Expected profit: ", expected_profit)
            if expected_profit > 0:
                self.choose_crop(crop_id)

    def choose_crop(self, new_id: int) -> bool:
        self.crop_id = new_id
        self.crop = self.model.crop_shop.crops[new_id]
        if self.budget >= self.crop.seed_cost:
            self.budget -= self.crop.seed_cost
            print(
                f"Farmer {self.id} changed crop to {self.crop_id}. New Budget: {self.budget}"
            )
        else:
            print(
                f"Farmer {self.id} could not change crop to {self.crop_id}. Budget was short!"
            )

    def farm(self):
        self._stock[self.crop_id] += self.crop.harvest_yield
        print(f"Farmer {self.id} harvested. New Stock: {self._stock}")

    def calc_supply(self, prices: Dict[int, int]) -> Dict[int, int]:
        """
        Calculates how much the farmer wants to supply

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
            supplies[crop_id] = np.min([self.c_agent[crop_id] * prices[crop_id], self._stock[crop_id]])
        self.supply = supplies
        return supplies

    def sell(self, crop_id: int, amount: int):
        if self._stock[crop_id] >= amount > 0:
            self._stock[crop_id] -= amount
            self.budget += amount * self.crop.sell_price
            print(
                f"Farmer {self.id} Sold {amount} of crop {crop_id}. New Stock: {self._stock}. New Budget: {self.budget}"
            )
        elif amount == 0.0:
            print(f"Nothing to sell.")
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
