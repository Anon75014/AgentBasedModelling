""" This file contains the Farmer Baseclass and Cell classes. """

import copy
from abc import ABCMeta, abstractmethod
from typing import Dict

import agentpy as ap
import numpy as np


class Cell(ap.Agent):
    def setup(self):
        """Setup the cells initial properties."""

        """Initiate agent reference attributes."""
        self.grid = self.model.grid
        self.random = self.model.random

        """ Set Cell variables """
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
        self.farmer._stock[self.crop._id] += self.crop.get_harvest_yield(self.farmer.water_supply / self.farmer.water_need)

    def set_farmer_id(self):
        """Used to extract the farmer id easily."""
        if self.farmer == -1:
            self.farmer_id = -1
        elif self.farmer:
            self.farmer_id = self.farmer.id
        else:
            self.farmer_id = 0


class BaseFarmer(ap.Agent):
    __metaclass__ = ABCMeta
    """Base Class for the Farmer with necessary farmer functionality."""

    # Optimize Todos :
    # - TODO choice of infodict keys

    """Necessary personality properties"""

    # INFO : this must be defined by each Farmer Personality
    @property
    @abstractmethod
    def personality_traits(self):
        """Personality traits that must be specified in subclass."""
        self.ml_controlled = False

        self.c_agent = {
            k: self.model.p.farmer_price_elasticity * self.model.random.random() for k in self.model.crop_shop.crops
        }
        self.buy_cell_threash = 1  # self.random.uniform(0, 1)  # for DQN v0
        self.crop_id_init = self.random.randint(0, len(self.model.crop_shop.crops) - 1)
        # TODO choice of infodict keys
        # -1 since len is  >= 1 and crop id starts at 0

    """Setting up the farmer agent"""

    def setup(self):
        """This function intitalises the necessary parameters for each farmer."""

        """Inherit agent attributes."""
        self.grid = self.model.grid
        self.random = self.model.random
        
        # INFO : the personality_traits function must be defined by each Farmer Personality
        self.personality_traits()

        """Setup neccessary agent attributes."""
        self.sourrounding = []  # list of accessible land coords
        self.aquired_land = []  # list of owned land coords
        self.budget = self.p.start_budget
        self.moneytracker = {"expansion_cost": 0, "crop_change": 0, "harvest_income": 0}
        self.crop = None
        self.cells = None
        self.cellcount = 0
        self._stock = {}  # setup and initiate stock = 0
        for crop_id in self.model.crop_shop.crops.keys():
            self._stock[crop_id] = self.model.p.farmer_starting_stock
        self.stock = copy.deepcopy(self._stock)  # this is recorded...
        self.supply = dict.fromkeys(self.model.crop_shop.crops.keys())

        """ Choose start position for Farmer"""
        if self.p.v0_pos and self.p.n_farmers == 4:
            pos_init = self.p.v0_pos.pop(0)
        else:
            pos_init = self.random.choice(self.model.unoccupied)

        self.model.unoccupied.remove(pos_init)

        """ Set start crop id"""
        self.crop = self.model.crop_shop.crops[self.crop_id_init]
        self.water_need = self.crop.water_need
        self.water_supply = None

        self._buy_cell(pos_init)
        self.change_to_crop(self.crop_id_init)

    """Necessary (private) Functions"""

    def _update_cell_list(self):
        """Update the list of a farmers cells."""
        self.cells = self.model.cells.select(self.model.cells.farmer == self)

    def _update_sourrounding(self):
        """Generate complete list of the sourrounding cells of a farmers property."""
        for _cell in self.cells:
            _cell_neighbours = self.grid.neighbors(_cell, distance=1)
            for _neighbor_cell in _cell_neighbours:
                if (
                    _neighbor_cell.farmer == None
                    and _neighbor_cell.pos not in self.sourrounding
                ):
                    self.sourrounding.append(_neighbor_cell.pos)

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

    def _buy_cell(self, _coordinates):
        """Farmer buys a cell at _coordinates and adds it to list."""
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
        self.model.cell_at(_coordinates).farmer = self

        # update list of the Farmers owned cells
        self._update_cell_list()
        self._update_sourrounding()

    """Basic Functions for (inter-)actions"""

    def update(self):
        """Update the farmers properties: cellcount, stock, crop_id for recording."""
        self.cellcount = len(self.cells)
        self.stock = copy.deepcopy(self._stock)
        self.crop_id = copy.deepcopy(self.crop._id)

    def find_and_buy(self, water_level: float, dir: str):
        """Find and buy a cell of water level "water_level" in direction "dir"
        relative to the inital position of the farmer.

        :param water_level: either 0.25, 0.5, 1
        :type water_level: float
        :param dir: direction, one of 'N','S','W','O'
        :type dir: str
        """
        _pos = self._find_matching_cell(water_level, dir)
        if _pos:
            self._buy_cell(_pos)

        print(f"Farmer {self.id} bought new land at {_pos}.")

    def change_to_crop(self, new_id: int):
        """Farmer changes all his cells to new crop new_id.

        :param new_id: [description]
        :type new_id: int
        """

        # Implemented Rules:
        # He can only change to a new one,
        # if he can buy the new crop seeds for all his cells
        # if the new_id is the same as the current one, onnly for cells with currently
        # no crop (crop_id == -1) new ones will be bought and planted

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
        """Sets the Farmers water supply from the river.

        :return: [description]
        :rtype: float
        """
        self.water_supply = self.model.river.get_water(self.water_need)
        #print(f"Farmer {self.id} obtained {self.water_supply} water units")
        return self.water_supply

    def harvest(self):
        """The Farmer updates the water supply from the river, then harvests all cells."""
        self.get_water_from_river()
        self.cells.harvest()
        # print(f"Farmer {self.id} harvested. New Stock: {self._stock}")

    def sell(self, crop_id: int, amount: int):
        """The specified amount of crop "crop_id" will be sold, if enough in stock.

        :param crop_id: ID of the crop to sell
        :type crop_id: int
        :param amount: amount of the crop that should be sold
        :type amount: int
        """
        if self._stock[crop_id] >= amount:
            # The farmer got enogh and can sell the specified amount
            self._stock[crop_id] -= amount

            self.budget += amount * self.crop.sell_price
            self.moneytracker["harvest_income"] += amount * self.crop.sell_price

    """Advanced, Personal Functions that depend on Personality"""

    # INFO : this must be defined by each Farmer Personality
    @property
    @abstractmethod
    def calc_supply(self, prices: Dict[int, int]) -> Dict[int, int]:
        """Calculates how much the farmer wants to supply

        :param prices: Dictionary with the global prices for each `crop_id`
        :type prices: Dict[int, int]
        :return: Dictionary with the amounts that the agent supplies
        :rtype: Dict[int, int]
        """

    # INFO : this function must be defined by each Farmer Personality
    @property
    @abstractmethod
    def pre_market_step(self):
        """Used to step the agent: eg. do the following: harvest -> define their supply"""

    # INFO : the step function must be defined by each Farmer Personality
    @property
    @abstractmethod
    def post_market_step(self):
        """Used to do strategic actions: e.g. change crop, expand"""
