""" This file contains the Agent and Cell classes. """

import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass

import agentpy as ap
import numpy as np


class Farmer(ap.Agent):
    def setup(self):
        """Initiate agent attributes."""
        self.grid = self.model.grid
        self.random = self.model.random
        self.buy_cell_threash = self.random.uniform(0,0.7) # TODO find good values

        """ Choose start position for Farmer"""
        self.sourrounding = []
        self.accuired_land = []
        self.pos_init = self.random.choice(self.model.unoccupied)
        self._buy_cell(self.pos_init)

        # Set start budget
        self.budget = self.p.start_budget

        # Set start crop
        self.crop_id = self.random.randint(
            0, len(self.model.crop_shop.crops) - 1
        )  # -1 since len is  >= 1 and crop id starts at 0
        self._change_to_crop(self.crop_id)

        # Initialise Stock dictionary
        self._stock = {}
        for crop_id in self.model.crop_shop.crops.keys():
            self._stock[crop_id] = 0

        self.stock = copy.deepcopy(self._stock)  # this is recorded...

    def _update_cell_list(self):
        self.cells = self.model.cells.select(
            self.model.cells.farmer_id == self.id)

    def _update_sourrounding(self):
        for _cell in self.cells:
            _cell_neighbours = self.grid.neighbors(_cell, distance=1)
            for _neighbor_cell in _cell_neighbours:
                if _neighbor_cell.farmer_id == 0 and \
                        _neighbor_cell.pos not in self.sourrounding:
                    self.sourrounding.append(_neighbor_cell.pos)

    def _buy_cell(self, _coordinates): #TODO add prices for cells!!!
        """Farmer buys a cell at _coordinates and adds it to list"""
        # TODO maybe not good if cells can be sold again. Why not track obscured cells, eg by water ::
        #self.model.unoccupied.remove(_coordinates)  
        self.accuired_land.append(_coordinates)

        # update cell properties
        self.model.cell_at(_coordinates).farmer_id = self.id
        self.model.cell_at(_coordinates).farmer = self
        self.model.cell_at(_coordinates).crop_id = self.crop_id
        self.model.cell_at(_coordinates).crop = self.crop
        
        # update list of the Farmers owned cells
        self._update_cell_list()
        self._update_sourrounding()

    def _change_to_crop(self, new_id: int):
        '''Farmer changes all his cells to new crop "new_id"'''
        self.crop_id = new_id
        self.crop = self.model.crop_shop.crops[new_id]
        self.budget -= self.crop.seed_cost * len(self.accuired_land)

        # update cell properties
        self.cells.crop_id = self.crop_id
        self.cells.crop = self.crop

        print(
            f"Farmer {self.id} changed crop to {self.crop_id}. New Budget: {self.budget}"
        )

    def harvest(self):
        self.cells.harvest()

        # print(f"Farmer {self.id} harvested. New Stock: {self._stock}")

    def sell(self, crop_id: int, amount: int):
        if self._stock[crop_id] >= amount:
            self._stock[crop_id] -= amount
            self.budget += amount * self.crop.sell_price
            print(
                f"Farmer {self.id} Sold {amount} of crop {crop_id}. New Stock: {self._stock}. New Budget: {self.budget}"
            )
        # else:
        #     print(
        #         f"Ups: Farmer {self.id} does not have enough in _stock for that deal."
        #     )

    def _get_next_from_direction(self, _dir: str, _a: int, _b: int):
        """ Converts the input so that it matches the direction
        Parameters:
        - _a is the slowly changing index
        - _b is the fast chaning index
        """

        N = self.model.n - 1
        M = self.model.m - 1

        functions = {
            'S': lambda a, b: tuple((a, M-b)),
            'W': lambda a, b: tuple((b, a)),
            'N': lambda a, b: tuple((N-a, b)),
            'O': lambda a, b: tuple((N-a, M-b)),
        }
        return functions[_dir](_a, _b)  # TODO Check if this works as expected

    def _find_matching_cell(self, _water_level: float, _dir: str):
        water_map = np.array(self.grid.attr_grid("water"))
        # create bitmap four available cells
        sourrounding_map = np.zeros_like(water_map, dtype=bool)
        for coord in self.sourrounding:
            sourrounding_map[coord] = True

        for slow in range(self.model.n):
            for fast in range(self.model.m):
                (i, j) = self._get_next_from_direction(_dir, slow, fast)
                if sourrounding_map[(i, j)]:
                    if self.model.cell_at((i, j)).water == _water_level:
                        return (i, j)

    def find_and_buy(self, water_level: float, dir: str):
        _pos = self._find_matching_cell(water_level, dir)
        self._buy_cell(_pos)
        
        print(f"Farmer {self.id} bought new land at {_pos}.")

    ''' Commands accessible by the CropWar model Class '''

    def step(self):
        self.harvest()

        amount = self.random.randint(0, 5)
        self.sell(self.crop_id, amount)

        dir = self.random.choice(self.model.headings)
        prob = self.random.uniform(0,1)
        if prob > self.buy_cell_threash: #TODO is that good?
            self.find_and_buy(1,dir) #TODO set water level

        # print(f"Stepped farmer {self.id}")

    def update(self):
        self.stock = copy.deepcopy(self._stock)


class Cell(ap.Agent):
    def setup(self):
        """Initiate agent attributes."""
        self.grid = self.model.grid
        self.random = self.model.random

        # Set variables
        self.farmer_id = 0  # legend: 0=empty,-1=unavailable, x>0 = farmer
        self.farmer = None
        self.crop = -1
        self.crop_id = -1
        self.pos = self.model.free_cell_coords.pop(0)
        self.water = self.model.water_matrix[self.pos]  # in [0,1] interval
        # self.is_border = True  # not quite sure if this var is necessary

    def harvest(self):
        self.farmer._stock[self.crop_id] += self.crop.harvest_yield

    def step(self):
        pass


class FarmerPersonality(ABC):
    """
    Abstract base class for the personalities of the farmers

    --> Each personality refers to a certain strategy interaction for the market or expansion (to be implemented).
    """

    # Aaron: Some dummy methods, replace them with the actual decisions
    @abstractmethod
    def buy(self) -> bool:
        """Buy something"""

    @abstractmethod
    def sell(self) -> bool:
        """Sell something"""


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
