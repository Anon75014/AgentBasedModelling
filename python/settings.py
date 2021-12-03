from agents import *
from ml_agents import *

experiment_settings = {
    "ML_Introvert_vs_3_Trader": {
        "saved_ML_models": [],
        "base_parameters": {
            # ---- MAP ----
            "water_levels": [0, 0, 3],
            # "v0_pos" : None,
            "v0_pos": sorted(
                [
                    (1, 1),
                    (1, 4),
                    (5, 1),
                    (5, 4),
                ],
                key=lambda x: x[0],
            ),
            # ---- General Simulation Settings ----
            "crop_shop": None,
            "amount_of_crops": None,
            "steps": 50,  # Amount of time steps
            "diagonal expansion": False,  # Only expand along edges
            "save_gif": False,  # Save map as Gif
            "seed": 0,  # Use a new seed
            # "seed" : b'\xad\x16\xf3\xa7\x116\x10\x05\xc7\x1f'      # Use a custom seed
            "farmers": {Trader: 3, Introvert: 0, ML_Introvert: 1},
            # ---- ML Parameters ----
            "ml_env": None,  # spec in RL_env
            "trainee_type" : None,
            "use_trained_model": False,
            # ---- Parameters ----
            "seed" : b'\x92\xbb\xce\x80\x03\x91\xfa\xa1\x7fi' ,    # Use a custom seed
            "nr_ml_farmers": 0,
            "farmers": {Trader: 2, Introvert: 2, ML_Introvert: 0},
            "max_stock": 2000.0,
            "max_budget": 1e8,
            "start_budget": 1000.,
            "river_content": 100.0,
            "market_base_demand": 400.0,
            "market_base_supply": 0.0,
            "market_demand_fraction": 0.5,
            "market_max_price": 1000000000000000000.0,
            "market_max_price": 1000.0,
            "market_demand_growth_factor": 0.05,
            "market_price_sensitivity": 2.5,
            "farmer_price_elasticity": 10.0,
            "farmer_starting_stock": 0.0,
            "farmer_starting_stock": 100.0,
        },
    }
}
