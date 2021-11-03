""" This file contains the Main structure of the Simulation. -> The AgentPy model """

import agentpy as ap
from agents import Farmer, Cell


class CropwarModel(ap.Model):
    """An Agent-Based-Model to simulate the crop war of farmers."""

    # See documentation https://agentpy.readthedocs.io/en/latest/reference_grid.html#agentpy.Grid

    def setup(self):
        """Setting parameters and model properties"""
        self.crop_shop = self.p.crop_shop
        
        water_row = sum(self.p.water_levels)  # ensure that water is in the center
        m = 2 * sum(self.p.water_levels)  # because these maps are symmetric
        n = m + 1  # and have one horizontal river (with thickness = 1)

        # Create grid:
        self.grid = ap.Grid(self, (n, m), track_empty=True)
        # Remove water coordinates from the grid s.t. no farmer is placed there and cannot cross it:
        for i in range(m):
            # print(f"This model got water at: {(water_row,i)} ?!")
            self.grid.empty.remove((water_row, i))

        n_farmers = self.p.n_farmers  # amount of farmer-agents
        self.agents = ap.AgentList(self, n_farmers, Farmer)

        n_cells = m*m           # amount of cells (that are not water)
        self.grid.add_agents(
            self.agents,
            #positions=[(5, 4), (5, 1), (1, 1), (1, 4)],
            random=True,
            empty=True,
        )  # version 0

        
        # self.grid.add_agents(self.agents, random=True, empty=True) # version 1
        print("Done: setup of grid.")

    def step(self):
        if self.t > self.p.t_end:  # model should stop after "t_end" steps
            self.stop()

        print(f"\n    Start of time step: {self.t}")
        self.agents.step()

    def update(self):
        # record the properties of the agents each step:
        self.agents.record("budget")
        self.agents.record("crop_id")
        self.agents.record("stock")

    def end(self):
        pass
