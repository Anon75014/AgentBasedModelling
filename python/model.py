""" This file contains the Main structure of the Simulation. -> The AgentPy model """

import agentpy as ap
from agents import Farmer, Cell
from copy import deepcopy
import numpy as np


class CropwarModel(ap.Model):
    """An Agent-Based-Model to simulate the crop war of farmers."""

    # See documentation https://agentpy.readthedocs.io/en/latest/reference_grid.html#agentpy.Grid

    def setup(self):
        """Setting parameters and model properties"""
        self.crop_shop = self.p.crop_shop
        self.water_row = sum(self.p.water_levels)  # <- index of center row
        # because these water rows are symmetric
        m = 2 * sum(self.p.water_levels)
        n = m + 1  # and have one horizontal river (with thickness = 1)

        """ Create grid: """
        self.grid = ap.Grid(self, (n, m), track_empty=True)
        # list of map coords: [(0,0),(0,1),...] :
        self.unoccupied = np.array(deepcopy(self.grid.empty))
        # self.ref_cell_indices = deepcopy(list(self.grid.empty)) # TODO needed?!
        self.water_matrix = self.generate_water_matrix()

        """ Initialising Cells"""
        n_cells = m * n  # amount of cells (that can even be water)
        self.free_cell_coords = deepcopy(list(self.grid.empty))
        # Dlist s.t. order is maintained
        self.cells = ap.AgentDList(self, n_cells, Cell)
        # check that all cells are assigned a position:
        assert len(self.free_cell_coords) == 0

        self.grid.add_agents(
            self.cells,
            # list of all positions = [(0,0),(0,1),...]
            positions=self.cells.pos,  # version 1.2
            random=False,
            empty=True,  # should give error if cell assignment was wrong
        )

        self._cell_dict = {v: k for k, v in self.grid.positions.items()}

        # Set River Cells
        for i in range(m):
            self.get_cell((self.water_row, i)).farmer_id = -1

        """ Initialising Farmers"""
        self.unoccupied = self.unoccupied[
            np.array(self.cells.farmer_id) == 0
        ].tolist()  # avoid river cells
        n_farmers = self.p.n_farmers  # amount of farmer-agents
        self.farmers = ap.AgentDList(self, n_farmers, Farmer)

        # dicitonary, mapping each matrix coordinate to the corresponding cell
        # self.grid.add_agents(self.agents, random=True, empty=True) # version 1
        print("Done: setup of grid.")

    def get_cell(self, pos: tuple):
        """Returns cell at pos Position in Grid"""
        return self._cell_dict[tuple(pos)]

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

    def step(self):
        if self.t > self.p.t_end:  # model should stop after "t_end" steps
            self.stop()
        print(f"\n    Start of time step: {self.t}")

        self.farmers.step()  # TODO

    def update(self):
        # record the properties of the farmers each step:
        self.farmers.update()
        self.farmers.record("budget")
        self.farmers.record("crop_id")
        self.farmers.record("stock")

    def end(self):
        pass
