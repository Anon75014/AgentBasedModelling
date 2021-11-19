""" This file contains the Main structure of the Simulation. -> The AgentPy model """

import os
from copy import deepcopy

import agentpy as ap
import numpy as np
from PIL import Image

import map_presenter
from agents import Cell, Farmer


class CropwarModel(ap.Model):
    """An Agent-Based-Model to simulate the crop war of farmers."""

    # See documentation https://agentpy.readthedocs.io/en/latest/reference_grid.html#agentpy.Grid

    def setup(self):
        """Setting random seed (for reproducibility)"""
        if self.p.seed == 0:
            self.p.seed = os.urandom(10)  # a random seed of length
        self.random.seed(self.p.seed)
        """Setting parameters and model properties"""
        self.crop_shop = self.p.crop_shop
        self.water_row = sum(self.p.water_levels)  # <- index of center row
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

        n_farmers = self.p.n_farmers  # amount of farmer-agents
        self.farmers = ap.AgentDList(self, n_farmers, Farmer)
        ml_mask = np.array(
            [False for _ in range(n_farmers - self.p.nr_ml_farmers)]
            + [True for _ in range(self.p.nr_ml_farmers)],
            dtype=bool,
        )
        self.farmers.select(ml_mask).ml_controlled = True
        self.ml_farmers = self.farmers.select(self.farmers.ml_controlled == True)
        self.normal_farmers = self.farmers.select(self.farmers.ml_controlled == False)

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

        print("Done: setup of grid.")

    def cell_at(self, pos: tuple):
        """Returns cell at pos Position in Grid"""
        return self._cell_dict[pos]

    def generate_water_matrix(self):
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

    def _valid_root_cell(self, farmer: Farmer, pos: tuple, _dir: str):
        """Check if one step into direction _dir the farmer ownes a cell"""
        for item in self._one_to_dir.values():
            if item(pos[0], pos[1]) in farmer.accuired_land:
                return True
        return False

    def step(self):
        if self.t > self.p.t_end:  # model should stop after "t_end" steps
            self.stop()
        print(f"\n    Start of time step: {self.t}")

        self.normal_farmers.step()

    def ml_get_state(self):
        pass
    def ml_step(self, action):
        pass

    def update(self):
        # record the properties of the farmers each step:
        self.farmers.update()
        self.farmers.record("budget")
        self.farmers.record("crop_id")
        self.farmers.record("stock")
        self.farmers.record("cellcount")

        if self.p.save_gif:
            self.cells.set_farmer_id()
            self.map_drawer.place_farmers()
            pil_map_img = self.map_drawer.show(return_img=True)
            # {self.t}.png","PNG")
            self.images_path = os.path.dirname(os.path.abspath(__file__)) + "/images/"
            file_path = self.images_path + "gif_frame.png"
            # pil_map_img.save(
            #     file_path,
            #     "PNG",
            # )
            self.map_frames.append(pil_map_img.convert("P", palette=Image.ADAPTIVE))

    def end(self):
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
