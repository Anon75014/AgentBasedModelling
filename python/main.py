""" Main File for the CropWar agent Based Simulation. """
# %%

from crops import CropSortiment
from graph_presenter import graph_class
from map_presenter import map_class
from model import CropwarModel

# These 2 lines are useful when working with Jupyter in vscode -> ask chris for help
# %load_ext autoreload
# %autoreload 2

if __name__ == "__main__":
    # The following parameters are provided to the Model instance and are accessible within the model by eg "self.p.water_levels"

    # The Crop_Shop contains the relevant information for the farmers.
    crop_shop = CropSortiment()
    # TODO Find good parameters for crops.
    crop_shop.add_crop(100, 15, 2)
    crop_shop.add_crop(150, 25, 1)

    parameters = {
        "water_levels": [1, 2, 3],
        "n_farmers": 4,
        "start_budget": 500,
        "t_end": 4,
        "crop_shop": crop_shop,
        "amount_of_crops": crop_shop.amount_of_crops,
    }

    """ Create and run the model """
    model = CropwarModel(parameters)  # create model instance

    results = model.run()
    print(f"The results are {results}.")
    print(results.variables.Farmer)
    print(f"The farmers got this land: {list(model.farmers.accuired_land)}")

    """ Display the results using the Displayer Class """
    presenter = graph_class(results)

    presenter.crops()
    presenter.stocks()
    presenter.budget()
    presenter.export()

    """ Display the Map with the farmers """

    # TODO at a later stage, when the farmers can expand etc we might want to track similar properties.
    mapper = map_class(model)
    mapper.add_farmers()
    mapper.show()

# %%
