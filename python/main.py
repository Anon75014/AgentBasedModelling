""" Main File for the CropWar agent Based Simulation. """

from pandas import DataFrame as df
from stable_baselines3 import PPO

from agents import *
from crops import *
from graph_presenter import graph_class
from map_presenter import map_class
from model import CropwarModel
from RL_agents import *
from settings import experiment_settings


def run_full_simulation(custom_parameters=None):
    """Run Simulation of the model and display results

    Run a full Simulation of the CropWar model and display resulting graphs and map.txt
    Infos: The 'parameters' are provided to the Model instance and are accessible within the model by eg "self.p.water_levels"
    The Crop_Shop contains the relevant information for the farmers.
    :param custom_parameters: dictionary of new parameters that should be used
    :type custom_parameters: dict, optional
    """
    crop_shop = CropSortiment()

    crop_shop.add_crop(WinterWheat)
    crop_shop.add_crop(Barley)
    crop_shop.add_crop(Maize)
    crop_shop.add_crop(Beans)
    ml_model = PPO.load("ML_agent_model")

    parameters = experiment_settings["ML_Introvert_vs_3_Trader"]["base_parameters"]
    parameters.update(
        {
            "crop_shop": crop_shop,
            "amount_of_crops": crop_shop.amount_of_crops,
            "use_trained_model": ml_model,
            "farmers": {Trader: 3, Introvert: 0, ML_Expander: 1},
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
    # presenter.traits(model)
    # presenter.personalities()
    presenter.prices()
    presenter.demand()
    presenter.supply()
    presenter.global_stock()

    for farmer in model.farmers:
        if farmer.type[:2] == "ML":
            print(f"Farmer {farmer.id} got total reward: {farmer.total_reward}")

    print(f"SEED: {model.p.seed}")
    """ Display the Map with the farmers """
    mapper = map_class(model)
    mapper.initialise_farmers()
    mapper.place_farmers()
    mapper.show()


if __name__ == "__main__":
    run_full_simulation()
