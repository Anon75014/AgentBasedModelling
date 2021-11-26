""" This file contains the Agent and Cell classes. """

import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

import agentpy as ap
import numpy as np


class Farmer(ap.Agent):
    """Farmer Class containing functions that CropWar farmers can do. :)
    Numerical Todos :
    - TODO better values for buy_cell_threash
    - TODO check and adjust prices for cells

    Technical Todos:
    - Done: change ALL positions to tuples s.t. no conversions necessary
    - Done: find good order to get new land... buy->crop or other way?
    - Done: remove farmer_id from cells. Do it via farmer.id
    - Done: remove all seperate crop_id of cells. Access it via crop._id
    - Done: "functions" are generated every check. maybe make this a model's property
    """

    def setup(self):

        self.ml_controlled = False

        """Inherit agent attributes."""
        self.grid = self.model.grid
        self.random = self.model.random
        self.c_agent = {  # TODO re-place
            k: 0.001 * self.model.random.random() for k in self.model.crop_shop.crops
        }  # TODO: find good values

        """ Setup neccessary agent attributes. """
        self.sourrounding = []  # list of accessible land coords
        self.aquired_land = []  # list of owned land coords
        self.budget = self.p.start_budget
        self.moneytracker = {"expansion_cost": 0, "crop_change": 0, "harvest_income": 0}
        self.crop = None
        self.cells = None
        self.cellcount = 0
        self._stock = {}  # setup and initiate stock = 0
        for crop_id in self.model.crop_shop.crops.keys():
            self._stock[crop_id] = 0
        self.stock = copy.deepcopy(self._stock)  # this is recorded...
        self.supply = dict.fromkeys(self.model.crop_shop.crops.keys())

        """ Choose start position for Farmer"""
        if self.p.v0_pos and self.p.n_farmers == 4:
            pos_init = self.p.v0_pos.pop(0)
        else:
            pos_init = self.random.choice(self.model.unoccupied)

        self.model.unoccupied.remove(pos_init)
        self.buy_cell_threash = self.random.uniform(0, 1) ## for DQN v0

        """ Set start crop id"""
        crop_id_init = self.random.randint(
            0, len(self.model.crop_shop.crops) - 1
        )  # -1 since len is  >= 1 and crop id starts at 0
        self.crop = self.model.crop_shop.crops[crop_id_init]
        self.water_need = self.crop.water_need
        self.water_supply = None

        self._buy_cell(pos_init)
        self._change_to_crop(crop_id_init)

    def _update_cell_list(self):
        """Update the list of a farmers cells"""
        self.cells = self.model.cells.select(self.model.cells.farmer == self)

    def _update_sourrounding(self):
        """generate complete list of the sourrounding cells of a farmers property"""
        for _cell in self.cells:
            _cell_neighbours = self.grid.neighbors(_cell, distance=1)
            for _neighbor_cell in _cell_neighbours:
                if (
                    _neighbor_cell.farmer == None
                    and _neighbor_cell.pos not in self.sourrounding
                ):
                    self.sourrounding.append(_neighbor_cell.pos)

    def _buy_cell(self, _coordinates):
        """Farmer buys a cell at _coordinates and adds it to list"""
        # make sure algorithm found an empty cell:
        cell = self.model.cell_at(_coordinates)
        # assert cell.farmer == None  # if river, farmer == -1

        if self.budget <= cell.buy_cost:
            return  # farmer got not enough budget to buy this Cell

        self.budget -= cell.buy_cost
        self.moneytracker["expansion_cost"] += cell.buy_cost
        self.aquired_land.append(_coordinates)
        self.water_need = len(self.aquired_land) * self.crop.water_need

        # update cells Propietary properties
        # self.model.cell_at(_coordinates).farmer_id = self.id
        self.model.cell_at(_coordinates).farmer = self

        # update list of the Farmers owned cells
        self._update_cell_list()
        self._update_sourrounding()

    def _change_to_crop(self, new_id: int):
        """Farmer changes all his cells to new crop new_id

        Implemented Rules:
        - He can only change to a new one,
          if he can buy the new crop seeds for all his cells
        - if the new_id is the same as the current one, onnly for cells with currently
            no crop (crop_id == -1) new ones will be bought and planted
        """
        _new_crop = self.model.crop_shop.crops[new_id]

        if new_id == self.crop._id:  # same as current
            active_cells = self.cells.select(self.cells.crop == None)
        else:  # farmer just changed crops
            active_cells = self.cells

            if self.budget < _new_crop.seed_cost * len(active_cells):
                print("Not enough money to change crop.")
                return
            else:
                self.crop = _new_crop

                print(f"Farmer {self.id} changed crop to {self.crop._id}.")

        for _cell in active_cells:
            if self.budget >= _new_crop.seed_cost:
                self.budget -= _new_crop.seed_cost
                self.moneytracker["crop_change"] += _new_crop.seed_cost

                # update cell properties ::
                _cell.crop = self.crop
        self.water_need = len(self.aquired_land) * self.crop.water_need

    def get_water_from_river(self) -> float:
        self.water_supply = self.model.river.get_water(self.water_need)
        print(f"Farmer {self.id} obtained {self.water_supply} water units")
        return self.water_supply

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
            supplies[crop_id] = np.min(
                [self.c_agent[crop_id] * prices[crop_id], self._stock[crop_id]]
            )
        self.supply = supplies
        return supplies

    def check_crop_change(
        self,
        crop_id: int,
        price: int,
        current_demand: int,
        current_supply: int,
    ) -> None:
        if crop_id != self.crop_id:
            cost_seed_change = len(self.aquired_land) * self.model.crop_shop.crops[crop_id].seed_cost
            price = self.model.crop_shop.crops[crop_id].sell_price
            expected_profit = (
                cost_seed_change + (current_demand - current_supply) * price
            )
            print("Expected profit: ", expected_profit)
            if expected_profit > 0:
                self._change_to_crop(crop_id)

    def harvest(self):
        self.get_water_from_river()
        self.cells.harvest()
        # print(f"Farmer {self.id} harvested. New Stock: {self._stock}")

    def sell(self, crop_id: int, amount: int):
        if self._stock[crop_id] >= amount:
            self._stock[crop_id] -= amount

            self.budget += amount * self.crop.sell_price
            self.moneytracker["harvest_income"] += amount * self.crop.sell_price

            # print(
            #     f"Farmer {self.id} Sold {amount} of crop {crop_id}. New Stock: {self._stock}. New Budget: {self.budget}"
            # )
        else:
            # " Not enough stock. "
            pass

    def _find_matching_cell(self, _water_level: float, _dir: str):
        water_map = np.array(self.grid.attr_grid("water"))
        # create bitmap four available cells
        sourrounding_map = np.zeros_like(water_map, dtype=bool)
        for coord in self.sourrounding:
            sourrounding_map[coord] = True

        for slow in range(self.model.N):
            for fast in range(self.model.M):
                # (i,j) will be every value in the grid.
                (i, j) = self.model._approach_from[_dir](slow, fast)

                if sourrounding_map[(i, j)]:
                    cell = self.model.cell_at((i, j))
                    """ Check that the cell is valid 
                        Rule: Cell must share an edge, not just a vertex
                    """
                    if cell.water == _water_level and cell.farmer == None:
                        if self.model._valid_root_cell(self, (i, j), _dir):
                            return (i, j)

        return None

    def find_and_buy(self, water_level: float, dir: str):
        _pos = self._find_matching_cell(water_level, dir)
        if _pos:
            self._buy_cell(_pos)

        print(f"Farmer {self.id} bought new land at {_pos}.")

    """ Commands accessible by the CropWar model Class :: """

    def step(self):
        self.harvest()

        # """ sell with relative boundaries """
        # amount = int(self.random.randint(0, 20) / 100 * self._stock[self.crop._id])
        # """ or: sell with fixed boundaries """
        # amount = self.random.randint(0, 5)
        # self.sell(self.crop._id, amount)

        dir = self.random.choice(self.model.headings)
        prob = self.random.uniform(0, 1)
        if prob > self.buy_cell_threash:
            self.find_and_buy(1, dir)  # TODO set water level
            self._change_to_crop(self.crop._id)  # TODO for now crop is constant

        # print(f"Stepped farmer {self.id}")

    def update(self):
        self.cellcount = len(self.cells)
        self.stock = copy.deepcopy(self._stock)
        self.crop_id = copy.deepcopy(self.crop._id)


class Cell(ap.Agent):
    def setup(self):
        """Initiate agent attributes."""
        self.grid = self.model.grid
        self.random = self.model.random

        # Set variables
        # self.farmer_id = 0  # legend: 0=empty,-1=unavailable, x>0 = farmer
        self.farmer = None
        self.crop = None
        self.pos = self.model.free_cell_coords.pop(0)
        self.water = self.model.water_matrix[self.pos]  # in [0,1] interval
        self.buy_cost = self.water * 10

    def harvest(self):
        """Harvest the cells content into farmers stock

        Rule:
        - If there is no crop planted on this cell yet => no yield
        """

        if self.crop == None:
            # print(f"No crop planted here! {self.pos}")
            return
        self.farmer._stock[self.crop._id] += (
            self.farmer.water_supply / self.farmer.water_need * self.crop.harvest_yield
        )

    def step(self):
        pass

    def set_farmer_id(self):
        if self.farmer == -1:
            self.farmer_id = -1
        elif self.farmer:
            self.farmer_id = self.farmer.id
        else:
            self.farmer_id = 0


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


@dataclass
class Stocker(FarmerPersonality):

    # Can add parameters like this, with default values since this is a dataclass
    some_parameter: int = 3

    def buy(self) -> bool:
        pass

    def buy(self) -> bool:
        pass


@dataclass
class Seller(FarmerPersonality):

    # Can add parameters like this, with default values since this is a dataclass
    some_parameter: int = 3

    def buy(self) -> bool:
        pass

    def buy(self) -> bool:
        pass


@dataclass
class Pioneer(FarmerPersonality):
    # Strategy: decide whether to invest in seeds and harvest next period or to invest in land and harvest then.
    # Can add parameters like this, with default values since this is a dataclass
    some_parameter: int = 3

    def buy(self) -> bool:
        pass

    def buy(self) -> bool:
        pass


@dataclass
class Efficiency(FarmerPersonality):
    # Strategy: decide whether to invest in seeds and harvest or to invest in technology and thereby increase harvest_yield for all crops
    # Can add parameters like this, with default values since this is a dataclass
    some_parameter: int = 3

    def buy(self) -> bool:
        pass

    def buy(self) -> bool:
        pass


# %%
