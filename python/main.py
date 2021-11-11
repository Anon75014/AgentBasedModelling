""" Main File for the CropWar agent Based Simulation. """
# %%

import presentation
from crops import CropSortiment
from model_structure import CropwarModel
from sim_map import Map
from pandas import DataFrame as df

# These 2 lines are useful when working with Jupyter in vscode -> ask chris for help
# %load_ext autoreload
# %autoreload 2

if __name__ == "__main__":
    # The following parameters are provided to the Model instance and are accessible within the model by eg "self.p.water_levels"

    # The Crop_Shop contains the relevant information for the farmers.
    crop_shop = CropSortiment()
    # Add two crops TODO Find good parameters for crops.
    crop_shop.add_crop(100, 15, 10)
    crop_shop.add_crop(150, 25, 5)

    parameters = {
        # only hydrated land. Later maybe [1,2,3] or so
        "water_levels": [0, 0, 3],
        "n_farmers": 4,
        "start_budget": 500,
        "t_end": 10,
        "crop_shop": crop_shop,
        "amount_of_crops": crop_shop.amount_of_crops
    }

    """ Create and run the model """
    model = CropwarModel(parameters)  # create model instance
    results = model.run()
    print(f"The results are {results}.")
    print(results.variables.Farmer)

    ''' Display the results using the Displayer Class'''
    presenter = presentation.Displayer(results)

    presenter.crops()
    presenter.stocks()
    presenter.budget()
    presenter.export()

    ''' Display the Map with the farmers '''
    farmer_pos_list = list(
        model.grid.positions.values()
    )  # get the placement of the farmers.

    print(f"The farmers are at: {farmer_pos_list}")
    # TODO at a later stage, when the farmers can expand etc we might want to track similar properties. and update them each time step from within the model framework
    sim_map = Map(*parameters["water_levels"])
    sim_map.generate_map()
    sim_map.add_farmers(farmer_pos_list)
    sim_map.show()

# %%
