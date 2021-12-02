""" Main File for the CropWar agent Based Simulation. """
# %%
# %%

from agents import *
from ml_agents import *
from crops import *
from graph_presenter import graph_class
from map_presenter import map_class
from model import CropwarModel

""" TODOS:
# TODO Find good parameters for crops.
"""
from pandas import DataFrame as df

# These 2 lines are useful when working with Jupyter in vscode -> ask chris for help
# %load_ext autoreload
# %autoreload 2


def run_full_simulation(use_ml_model=False):
    """Run Simulation of the model and display results

    Run a full Simulation of the CropWar model and display resulting graphs and map.txt
    :param use_ml_model: specify wether a trained machine learning (ml) model should be used, defaults to False
    :type use_ml_model: bool, optional
    """
    # The following parameters are provided to the Model instance and are accessible within the model by eg "self.p.water_levels"

    # The Crop_Shop contains the relevant information for the farmers.
    crop_shop = CropSortiment()
    # Add two crops TODO Find good parameters for crops.

    crop_shop.add_crop(WinterWheat)
    crop_shop.add_crop(Barley)
    crop_shop.add_crop(Maize)
    crop_shop.add_crop(Beans)

    # These parameters are accessible within the model by"self.p.water_levels"
    parameters = {
        # FIXED:
        "crop_shop": crop_shop,
        "amount_of_crops": crop_shop.amount_of_crops,
        # TUNABLE:
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
        ),  # number of start positions must match n_farmers
        "start_budget": 1000,
        "steps": 50,  # Amount of time steps to be simulated
        "diagonal expansion": False,  # Only expand along the owned edges. like + and not x
        "save_gif": False,  # Save the map each timestep and generate Gif in the end
        #"seed": 0,  # Use a new seed
         "seed" : b'\x92\xbb\xce\x80\x03\x91\xfa\xa1\x7fi' ,    # Use a custom seed
        "nr_ml_farmers": 0,
        "farmers": {Trader: 4, Introvert: 0, ML_Introvert: 0},
        "use_trained_model": False,
        "max_stock": 200,
        "max_budget": 3000,
        "river_content": 100.0,
        "market_base_demand": 30.0,
        "market_base_supply": 0.0,
        "market_demand_fraction": 0.5,
        "market_max_price": 500.0,
        "farmer_price_elasticity": 100.0,
        "farmer_starting_stock": 0.0,
    }

    """ Create and run the model """
    model = CropwarModel(parameters)  # create model instance

    results = model.run()
    # print(f"The results are {results}.")
    # print(results.variables.Farmer)
    # print(f"The farmers got this land: {list(model.farmers.accuired_land)}")

    """ Display the results using the Displayer Class """
    presenter = graph_class(model, results)

    #presenter.crops()
    #presenter.cellcount()
    presenter.stocks()
    presenter.budget()
    #presenter.export()
    #presenter.traits(model)
    #presenter.personalities()
    presenter.prices()
    presenter.demand()
    presenter.supply()
    presenter.global_stock()
    import matplotlib.pyplot as plt
    plt.show()

    print(f"SEED: {model.p.seed}")

    """ Display the Map with the farmers """
    mapper = map_class(model)
    mapper.initialise_farmers()
    mapper.place_farmers()
    #mapper.show()

    print(f"SEED: {model.p.seed}")


# %%
if __name__ == "__main__":
    run_full_simulation()
