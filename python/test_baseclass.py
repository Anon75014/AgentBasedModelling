
import os

import agentpy as ap
import numpy as np
from PIL import Image

import map_presenter
from agents_base import BaseFarmer, Cell
from crops import CropSortiment
from market import Market
from river import River



class AggressiveFarmer(BaseFarmer):
    def personality_traits(self):
        self.ml_controlled = False

        self.c_agent = {
            k: 0.001 * self.model.random.random() for k in self.model.crop_shop.crops
        }
        self.buy_cell_threash = 1  # self.random.uniform(0, 1)  # for DQN v0
        self.crop_id_init = self.random.randint(
            0, len(self.model.crop_shop.crops) - 1
        )  # -1 since len is  >= 1 and crop id starts at 0

if __name__ == '__main__':
    
    crop_shop = CropSortiment()

    crop_shop.add_crop(1, 1, 1)  # area, crop_type, available water
    crop_shop.add_crop(1, 2, 1)  # area, crop_type, available water

    parameters = {
        # FIXED:
        "crop_shop": crop_shop,
        "amount_of_crops": crop_shop.amount_of_crops,
        # TUNABLE:
        "water_levels": [0, 0, 3],
        "n_farmers": 4,
        # "v0_pos" : None,
        "v0_pos": sorted([
            (1, 1),
            (1, 4),
            (5, 1),
            (5, 4),
        ], key=lambda x: x[0]),  # number of start positions must match n_farmers
        "start_budget": 1000,
        "t_end": 15,  # Amount of time steps to be simulated
        "diagonal expansion": False,  # Only expand along the owned edges. like + and not x
        "save_gif": True,  # Save the map each timestep and generate Gif in the end
        "seed": 0,  # Use a new seed
        # "seed" : b'\xad\x16\xf3\xa7\x116\x10\x05\xc7\x1f'      # Use a custom seed
        "nr_ml_farmers": 0,
        "use_trained_model": False,
        "max_stock": 200,
        "max_budget": 3000,
        "river_content": 12.0,
        "market_base_demand": 10.0,
        "market_demand_fraction": 0.7,
    }


    class ModelTest(ap.Model):
        def setup(self):
            self.p.seed = os.urandom(10)  # a random seed of length
            self.random.seed(self.p.seed)
            self.crop_shop = self.p.crop_shop
            self.grid = ap.Grid(self, (2, 2), track_empty=True)

        def test(self):
            self.farmers = ap.AgentList(self, 2, AggressiveFarmer)

    X = ModelTest(parameters)
    X.setup()
    X.test()
    print(X.farmers)
    print(X.farmers[0])

