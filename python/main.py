""" Main File for the CropWar agent Based Simulation. """
# %%
# %%

from agents import *
from crops import CropSortiment
from graph_presenter import graph_class
from map_presenter import map_class
from ml_agents import *
from model import CropwarModel
from settings import experiment_settings

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

    crop_shop.add_crop(1, 1, 1)  # area, crop_type, available water
    crop_shop.add_crop(1, 2, 1)  # area, crop_type, available water
    crop_shop.add_crop(1, 3, 1)  # area, crop_type, available water
    crop_shop.add_crop(1, 4, 1)  # area, crop_type, available water
    crop_shop.add_crop(1, 9, 1)

    # These parameters are accessible within the model by"self.p.water_levels"
    parameters = experiment_settings["Stationary_ML_vs_3_Trader"]["base_parameters"]
    parameters.update(
        {  # FIXED for main.py:
            "crop_shop": crop_shop,
            "amount_of_crops": crop_shop.amount_of_crops,
        }
    )

    """ Create and run the model """
    if use_ml_model:
        parameters["use_trained_model"] = use_ml_model

    model = CropwarModel(parameters)  # create model instance

    results = model.run()
    # print(f"The results are {results}.")
    # print(results.variables.Farmer)
    # print(f"The farmers got this land: {list(model.farmers.accuired_land)}")

    """ Display the results using the Displayer Class """
    presenter = graph_class(model, results)

    presenter.crops()
    presenter.cellcount()
    presenter.stocks()
    presenter.budget()
    presenter.export()
    # presenter.traits(model)
    presenter.personalities()
    presenter.prices()

    if use_ml_model:
        print(f"ML: Reached total reward: {model.total_reward}")

    print(f"SEED: {model.p.seed}")

    """ Display the Map with the farmers """
    mapper = map_class(model)
    mapper.initialise_farmers()
    mapper.place_farmers()
    mapper.show()

    print(f"SEED: {model.p.seed}")


# %%
if __name__ == "__main__":
    run_full_simulation()
