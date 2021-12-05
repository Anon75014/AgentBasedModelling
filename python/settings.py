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
            "steps": 300,  # Amount of time steps
            "diagonal expansion": False,  # Only expand along edges
            "save_gif": False,  # Save map as Gif
            "seed": b"\x92\xbb\xce\x80\x03\x91\xfa\xa1\x7fi",  # Use a custom seed
            "farmers": {Trader: 4, Introvert: 0, ML_Expander: 0},
            # ---- ML Parameters ----
            "ml_env": None,  # spec in RL_env
            "trainee_type": None,
            "use_trained_model": False,
            # ---- Parameters ----
            "max_stock": 2e5,
            "max_budget": 1e8,
            "start_budget": 500.0,
            "river_content": 100.0,
            "market_base_demand": 90.0,
            "market_base_supply": 50.0,
            "market_max_price": 1.0,
            "market_demand_growth_factor": 1e-3,
            "market_price_sensitivity": 1.0,
            "farmer_price_elasticity": 10.0,
            "farmer_starting_stock": 20.0,
        },
    }
}
