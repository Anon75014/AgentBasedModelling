""" This file contains the Main structure of the Simulation. -> The AgentPy model """

import agentpy as ap
from agents import Farmer


class CropwarModel(ap.Model):
    """ An Agent-Based-Model to simulate the crop war of farmers."""
    # See documentation https://agentpy.readthedocs.io/en/latest/reference_grid.html#agentpy.Grid

    def setup(self):
        """ Setting parameters and model properties """
        water_levels = self.p.water_levels  # self.p. ... access of provided paramter dictionary
        m = 2*sum(water_levels)             # because these maps are symmetric
        n = m+1                             # and have one horizontal river (with thickness = 1)
        water_row = sum(water_levels)       # ensure that water is in the center
        N_farmers = self.p.N_farmers        # amount of farmer-agents

        # Create grid: 
        self.grid = ap.Grid(self, (n,m), track_empty = True)

        # Remove water coordinates from the grid s.t. no farmer is placed there and cannot cross it:
        for i in range(m):
            #print(f"This model got water at: {(water_row,i)} ?!")
            self.grid.empty.remove((water_row,i))

        self.agents = ap.AgentList(self, N_farmers, Farmer)

        self.grid.add_agents(self.agents,positions=[(5,4),(5,1),(1,1),(1,4)], random=False, empty=True) # version 0
        # self.grid.add_agents(self.agents, random=True, empty=True) # version 1
        print('Done: setup of grid.')

    def update(self):
        if self.t > self.p.t_end:       # model should stop after "t_end" steps
            self.stop()
        self.agents.farm()              # agents should farm each step
        self.agents.record("budget")    # record these properties of the agents each step
        self.agents.record("crop_id")
        self.agents.record("stock")


    def step(self):
        pass

    def end(self):
        # These reporter functions can be used to track properties over multiple experiments. 
        # For example, which farmer personality got the most money, or the most stock, etc
        self.report('my_reporter', 1)   
        pass


