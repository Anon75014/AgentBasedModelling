""" Main File for the CropWar agent Based Simulation. """

from sim_map import Map
from model_structure import CropwarModel
from crops import CropSortiment


if __name__ == "__main__":
    # The following parameters are provided to the Model instance and are accessible within the model by eg "self.p.water_levels"

    # The Crop_Shop contains the relevant information for the farmers.
    crop_shop = CropSortiment()
    crop_shop.add_crop(100, 15, 2)  # Add two crops TODO Find good parameters for crops.
    crop_shop.add_crop(150, 25, 1)

    parameters = {
        "water_levels": [0, 0, 3],  # only hydrated land. Later maybe [1,2,3] or so
        "n_farmers": 4,
        "start_budget": 500,
        "t_end": 10,
        "crop_shop": crop_shop,
    }

    """ Create and run the model """
    model = CropwarModel(parameters)  # create model instance
    model.setup()  # setup the model and its properties
    farmer_pos_list = list(
        model.grid.positions.values()
    )  # get the placement of the farmers.
    print(f"The farmers are at: {farmer_pos_list}")
    # TODO at a later stage, when the farmers can expand etc we might want to track similar properties. and update them each time step from within the model framework

    results = model.run()
    print(f"The results are {results}.")
    # print(model.output['info'])
    # TODO see how the "record" function output can be displayed easily and beautiful

    """ Display the Map with the farmers """
    sim_map = Map(*parameters["water_levels"])
    sim_map.generate_map()
    sim_map.add_farmers(farmer_pos_list)
    sim_map.show()
