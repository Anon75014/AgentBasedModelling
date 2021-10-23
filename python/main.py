#%%

# info: these next two lines are useful when editing the sim_map file.
#       Just do  "Run Cell" and jupyter auto-reloads the sim_map file and generates the map with the updated code... :)
#       -> Maybe make them to comments when running this file without Jupyter Notebook...
%reload_ext autoreload
%autoreload 2


import numpy as np
import matplotlib.pyplot as plt
from sim_map import Map

if __name__ == '__main__':
    ## Version 0 map:
    #m = Map(2,1,0,0)
    
    ## Version 1 map:
    m = Map(13,1,2,3)

    m.generateMap()
    m.show()

