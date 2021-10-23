""" This file contains the Main structure of the Simulation. -> The AgentPy model """

import agentpy as ap
from agents import Farmer


class CropwarModel(ap.Model):

    def setup(self):
        # Parameters
        water_levels = self.p.water_levels
        m = 2*sum(water_levels); n = m+1
        water_row = sum(water_levels) # as the matrix index starts with 0... 
        N_farmers = self.p.N_farmers

        # Create grid and agents
        self.grid = ap.Grid(self, (n,m), track_empty = True)
        # Remove water coordinates from the grid s.t. no farmer is placed there and cannot cross it.
        for i in range(m):
            #print(f"Got water at:{(water_row,i)}")
            self.grid.empty.remove((water_row,i))

        self.agents = ap.AgentList(self, N_farmers, Farmer)
        self.grid.add_agents(self.agents,positions=[(5,4),(5,1),(1,1),(1,4)], random=False, empty=True)
        
        print('Done: setup of Grid.')

    def update(self):
        if self.t > 10:
            self.stop()
        self.agents.farm()
        self.agents.record("budget")
        self.agents.record("crop_id")
        self.agents.record("stock")


    def step(self):
        pass

    def end(self):
        self.report('my_reporter', 1)  # Report a simulation result #just a test
        pass
