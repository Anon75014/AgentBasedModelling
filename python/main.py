""" Main File for the CropWar agent Based Simulation. """
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


def run_full_simulation(custom_parameters=None):
    """Run Simulation of the model and display results

    Run a full Simulation of the CropWar model and display resulting graphs and map.txt
    Infos: The 'parameters' are provided to the Model instance and are accessible within the model by eg "self.p.water_levels"
    The Crop_Shop contains the relevant information for the farmers.
    :param custom_parameters: dictionary of new parameters that should be used 
    :type custom_parameters: dict, optional
    """
    # 
    crop_shop = CropSortiment()

    crop_shop.add_crop(1, 1, 1)  # area, crop_type, available water
    crop_shop.add_crop(1, 2, 1)  # area, crop_type, available water
    crop_shop.add_crop(1, 3, 1)  # area, crop_type, available water
    crop_shop.add_crop(1, 4, 1)  # area, crop_type, available water
    crop_shop.add_crop(1, 9, 1)

    parameters = experiment_settings["ML_Introvert_vs_3_Trader"]["base_parameters"]
    parameters.update(
        {
            "crop_shop": crop_shop,
            "amount_of_crops": crop_shop.amount_of_crops,
            # Set amounts of Deterministic / PreTrained farmers
            "farmers": {Trader: 2, Introvert: 2, ML_Introvert: 0},
        }
    )
    """Update Model Parameters"""
    if custom_parameters:
        parameters.update(custom_parameters)

    """ Create and run the model """
    model = CropwarModel(parameters)
    results = model.run()

    """ Display the results using the Displayer Class """
    presenter = graph_class(model, results)

    presenter.crops()
    presenter.cellcount()
    presenter.stocks()
    presenter.budget()
    presenter.export()
    presenter.personalities()
    presenter.prices()

    for farmer in model.farmers:
        if farmer.type[:2] == "ML":
            print(f"Farmer {farmer.id} got total reward: {farmer.total_reward}")

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
