# info: these next two lines  auto-reloads the sim_map file and generates the map with the updated code... :)
#  -> Make them to comments when running this file as a Jupyter Notebook...
#%reload_ext autoreload
#%autoreload 2

from sim_map import Map
from modelStructure import CropwarModel


def createMap(low,mid,high):        #just for developing with agentpy
    ## Version 0 map: 
    m = Map(2*(low+mid+high),low,mid,high)

    ## Version 1 map:
    #m = Map(13,1,2,3)

    m.generateMap()
    #m.show()  # To see the newly generated map
    return m



if __name__ == '__main__':
    parameters = {
        'water_levels' : [0,0,3],
        'N_farmers' : 4,
        'start_budget' : 500
    }

    model = CropwarModel(parameters)
    model.setup()
    farmer_pos_list = list(model.grid.positions.values())  # TODO beautify this @ chris
    res = model.run()
    print(res)
#    print(model.output['info']) # TODO see how the "record" function output can be displayed easily

    print(farmer_pos_list)
    map = createMap(*parameters['water_levels'])
    map.add_farmers(farmer_pos_list)
    map.show()


