""" Main File for the CropWar agent Based Simulation. """

from sim_map import Map
from modelStructure import CropwarModel


if __name__ == '__main__':
    # The following parameters are provided to the Model instance and are accessible within the model by eg "self.p.water_levels"
    parameters = {
        'water_levels' : [0,0,3], # only hydrated land. Later maybe [1,2,3] or so
        'N_farmers' : 4,
        'start_budget' : 500,
        't_end' : 10
    }

    ''' Create and run the model '''
    model = CropwarModel(parameters)                        # create model instance
    model.setup()                                           # setup the model and its properties
    farmer_pos_list = list(model.grid.positions.values())   # get the placement of the farmers.
    print(f"The farmers are at: {farmer_pos_list}")
    # TODO at a later stage, when the farmers can expand etc we might want to track similar properties. and update them each time step from within the model framework
    
    results = model.run()
    print(f"The results are {results}.")
    # print(model.output['info']) 
    # TODO see how the "record" function output can be displayed easily and beautiful

    
    """ Display the Map with the farmers """
    map = Map(*parameters['water_levels'])
    map.generateMap()
    map.add_farmers(farmer_pos_list)
    map.show()


