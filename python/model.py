""" This file contains the Main structure of the Simulation. -> The AgentPy model """
#%%
import os
from copy import deepcopy

import agentpy as ap
import numpy as np
from PIL import Image

import map_presenter
from agents_base import Cell
from agents import Trader
from ml_agents import ML_Introvert
from market import Market
from agents_base import BaseFarmer
from river import River

""" TODOS ::
"""


class CropwarModel(ap.Model):
    """AgentPy model used for simulation.

    An agent based model (ABM) to simulate competing farmers.
    :param parameters: dictionary of parameters, stored as self.p
    """

    # See documentation https://agentpy.readthedocs.io/en/latest/reference_grid.html#agentpy.Grid
    # def __init__(self,parameters) -> None:
    #     super().__init__(parameters)

    def setup(self):
        """Setting up of the ABM model."""

        """Setting random seed (for reproducibility)"""
        if self.p.seed == 0:
            self.p.seed = os.urandom(10)  # a random seed of length
        self.random.seed(self.p.seed)
        """Setting parameters and model properties"""
        self.crop_shop = self.p.crop_shop
        self.water_row = sum(self.p.water_levels)  # <- index of center row
        self.river = River(water_content=self.p.river_content)
        # because these water rows are symmetric
        m = 2 * sum(self.p.water_levels)
        n = m + 1  # and have one horizontal river (with thickness = 1)
        self.n = n  # amount of rows
        self.m = m
        self.N = n - 1  # max index
        self.M = m - 1  # max index

        """ Create grid: """
        self.grid = ap.Grid(self, (n, m), track_empty=True)
        # list of map coords: [(0,0),(0,1),...] ::
        self.unoccupied = np.array(deepcopy(self.grid.empty))
        self.water_matrix = self.generate_water_matrix()
        self.headings = ["N", "O", "S", "W"]

        """ Grid Iteration Functions """
        self._one_to_dir = {
            "S": lambda a, b: (a - 1, b),
            "W": lambda a, b: (a, b - 1),
            "N": lambda a, b: (a + 1, b),
            "O": lambda a, b: (a, b + 1),
        }
        """ About: _approach_from 
            Info: Converts the input so that it matches the direction
            Parameters:
                _a is the slowly changing index
                _b is the fast chaning index
        """
        self._approach_from = {
            "S": lambda a, b: (a, self.M - b),
            "W": lambda a, b: (b, a),
            "N": lambda a, b: (self.N - a, b),
            "O": lambda a, b: (self.N - a, self.M - b),
        }

        """ Initialising Cells"""
        n_cells = m * n  # amount of cells (that can even be water)
        self.free_cell_coords = deepcopy(list(self.grid.empty))
        # Dlist s.t. order is maintained ::
        self.cells = ap.AgentDList(self, n_cells, Cell)
        # check that all cells are assigned a position ::
        assert len(self.free_cell_coords) == 0

        self.grid.add_agents(  # CELLS
            self.cells,
            # list of all positions = [(0,0),(0,1),...] ::
            positions=self.cells.pos,  # version 1.2
            random=False,  # well defined positions exist
            empty=True,  # should give error if cell assignment was wrong
        )

        self._cell_dict = {v: k for k, v in self.grid.positions.items()}

        # Set River Cells
        for i in range(m):
            self.cell_at((self.water_row, i)).farmer = -1

        """ Initialising Farmers"""
        self.unoccupied = self.unoccupied[
            np.array(self.cells.farmer) == None
        ].tolist()  # avoid river cells
        self.unoccupied = [tuple(coord) for coord in self.unoccupied]

        self.p.n_farmers = sum(self.p.farmers.values())
        n_farmers = self.p.n_farmers  # amount of farmer-agents
        # TODO n_farmers NOT NEEDED HERE ANYMORE ONCE ML CODE Updated

        farmers = []
        for kind, amount in self.p.farmers.items():
            farmers += [kind] * amount
        self.random.shuffle(farmers)

        self.farmers = ap.AgentDList(self, 1, farmers.pop(0))
        for _ in range(self.p.n_farmers - 1):
            self.farmers += ap.AgentDList(self, 1, farmers.pop(0))
        # TODO check THIS FARMER SETUP

        """ MARKET """
        self.market = Market(
            crop_sortiment=self.crop_shop,
            agents=self.farmers,
            model=self,
            base_demand=self.p.market_base_demand,
            demand_fraction=self.p.market_demand_fraction,
            max_price=self.p.market_max_price,
            demand_growth_factor=self.p.market_demand_growth_factor,
            price_sensitivity=self.p.market_price_sensitivity,
        )
        self.crop_prices = self.market.current_prices.copy()
        self.price_history = []
        self.demand_history = []
        self.supply_history = []
        self.global_stock_history = []
        """ MACHINE LEARNING """
        self.time_is_up = False
        self.ml_trainee = None  # default
        # deterministic farmers:
        self.det_farmers = self.model.farmers.select(
            [name[:2] != "ML" for name in self.model.farmers.type]
        )
        nr_det = len(self.det_farmers)
        # if nr_det < self.p.n_farmers and nr_det + 1 == self.p.n_farmers:
        if self.p.farmers[ML_Introvert] == 1: # TODO or other ML_Type
            self.ml_trainee = self.model.farmers.select(
                [name[:2] == "ML" for name in self.model.farmers.type]
            )[0]
            self.p.ml_env.ml_trainee = self.ml_trainee
        elif self.p.farmers[ML_Introvert] > 1:
            raise ValueError("It seems like there is more than one ML trainee...")

        """ Initialise Map (for GIF) Instances """
        if self.p.save_gif:
            try:
                dirname = os.path.dirname(os.path.abspath(__file__))
                os.mkdir(dirname + "/images")
            except OSError as error:
                print(f"Folder exists already, so: {error}")
            self.map_frames = []  # used for png storage for the gif
            self.map_drawer = map_presenter.map_class(self)
            self.map_drawer.initialise_farmers()


    def cell_at(self, pos: tuple):
        """Returns cell at pos Position in Grid"""
        return self._cell_dict[pos]

    def generate_water_matrix(self) -> np.array:
        """Generates the hydration matrix.

        Generate the distribution of hydration cells throughout the map.
        :return: matrix containing the hydration leves; hydration = 0.25, 0.5, 1, water = 10
        :rtype: np.array
        """
        self._water_index = 10
        water = 1  # amount of water rows. MUST be 1 based on 'm' calculation in setup()

        # list of integers; len = 4
        amounts = np.concatenate((self.p.water_levels, [water]))
        weights = [0.25, 0.5, 1, self._water_index]

        """  Set water-matrix entries according to water levels"""
        water_matrix = np.ones(self.grid.shape)
        row = 0
        for index, amount in enumerate(amounts):
            for _ in range(amount):
                # based on symmetry color two rows at once
                water_matrix[row, :] = weights[index]
                water_matrix[-(row + 1), :] = weights[index]
                row += 1

        return water_matrix

    def _valid_root_cell(
        self, farmer: BaseFarmer, pos: tuple, _dir: str
    ):  # TODO CHeck if THIS baseFARMER ref works
        """Check if one step into direction _dir the farmer ownes a cell"""
        for item in self._one_to_dir.values():
            if item(pos[0], pos[1]) in farmer.aquired_land:
                return True
        return False

    def at_last_step(self) -> bool:
        """Check if at last time step.

        :rtype: bool
        """
        return self.t == self.p.t_end

    def step(self):
        """Move model from t to t+1.

        Evolve the entire model by one time step:
        - Step all the "normal" farmers
        - Step potentially trained farmers to
        - Step the market
        - let farmers decide if they want to change crops
        - refresh the river water content
        """
        # if self.t > self.p.t_end:  # model should stop after "t_end" steps
        #     self.time_is_up = True
        #     self.stop()  # end the current simulation

        self.farmers.pre_market_step()

        # if self.p.use_trained_model:
        #     obs, _ = self.ml_get_state()
        #     action, _ = self.p.use_trained_model.predict(obs, deterministic=True)
        #     self.ml_step(action)

        self.market.step()

        self.farmers.post_market_step()
        self.river.refresh_water_content()

    

    # def ml_step(self, action: np.array):
    #     """Applies action to environment.

    #     Applies the action decided by the ML algorithm to the environment.
    #     :param action: np.array of ints
    #     :type action: np.array
    #     """
    #     ml_farmer = self.ml_farmers[0]
    #     [do_farm, sell] = action
    #     if do_farm:
    #         ml_farmer.harvest()

    #     if sell:
    #         # TODO generalize 0.2 by making action continuous::
    #         amount = int(0.2 * ml_farmer._stock[ml_farmer.crop._id])

    #         ml_farmer.sell(ml_farmer.crop._id, amount)

    #     return

    def update(self):
        """Record the properties of the farmers each step."""
        self.farmers.update()
        self.farmers.record("budget")
        self.farmers.record("crop_id")
        self.farmers.record("stock")
        self.farmers.record("cellcount")
        self.price_history.append(list(self.market.current_prices.values()))
        self.demand_history.append(list(self.market.current_demand.values()))
        self.supply_history.append(list(self.market.current_supply.values()))
        self.global_stock_history.append(list(self.market.current_stock.values()))
        # self.record("crop_prices")

        if self.p.save_gif:
            self.cells.set_farmer_id()
            self.map_drawer.place_farmers()
            pil_map_img = self.map_drawer.show(return_img=True)
            self.images_path = os.path.dirname(os.path.abspath(__file__)) + "/images/"
            file_path = self.images_path + "gif_frame.png"

            self.map_frames.append(pil_map_img.convert("P", palette=Image.ADAPTIVE))

    def end(self):
        """Performs final action at the end."""
        self.cells.set_farmer_id()

        if self.p.save_gif:
            print(f"Found {len(self.map_frames)} images.")
            self.map_frames[0].save(
                self.images_path + "map.gif",
                save_all=True,
                append_images=self.map_frames[1:],
                optimize=True,
                duration=200,
                loop=3,
            )

    def _info_dict(self) -> dict:
        """Used to generate a dict so that the config can be saved into a json file."""
        _pars_dict = deepcopy(self.p)
        _pars_dict.crop_shop = _pars_dict.crop_shop._info_dict()
        _pars_dict.seed = str(_pars_dict.seed)
        return dict(_pars_dict)


# %%
