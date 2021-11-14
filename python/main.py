""" Main File for the CropWar agent Based Simulation. """
# %%

from crops import CropSortiment
from graph_presenter import graph_class
from map_presenter import map_class
from model import CropwarModel

""" TODOS:
# TODO Find good parameters for crops.

"""


# These 2 lines are useful when working with Jupyter in vscode
# # %load_ext autoreload
# %autoreload 2

if __name__ == "__main__":

    # The Crop_Shop contains the relevant crop informations for the farmers.
    crop_shop = CropSortiment()
    crop_shop.add_crop(100, 15, 2)
    crop_shop.add_crop(150, 25, 1)

    # These parameters are accessible within the model by"self.p.water_levels"
    parameters = {
        "water_levels": [0, 0, 3],
        "n_farmers": 4,
        # "v0_pos" : None,
        "v0_pos": [(5, 4), (5, 1), (1, 1), (1, 4)],
        "start_budget": 500,
        "t_end": 20,
        "crop_shop": crop_shop,
        "amount_of_crops": crop_shop.amount_of_crops,
        "diagonal expansion": False,
        "save_gif": True,
    }

    """ Create and run the model """
    model = CropwarModel(parameters)  # create model instance

    results = model.run()
    # print(f"The results are {results}.")
    print(results.variables.Farmer)
    # print(f"The farmers got this land: {list(model.farmers.accuired_land)}")

    """ Display the results using the Displayer Class """
    presenter = graph_class(results)

    presenter.crops()
    presenter.cellcount()
    presenter.stocks()
    presenter.budget()
    presenter.export()
    presenter.traits(model)

    """ Display the Map with the farmers """
    mapper = map_class(model)
    mapper.initialise_farmers()
    mapper.place_farmers()
    mapper.show()

# %%
