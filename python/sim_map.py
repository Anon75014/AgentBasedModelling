import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches # used for legend in plt plot

class Catchment: 
    """
    Catchments in which the farmers will compete
    """
    def __init__(self):
        pass

class Map:
    """
    Entire map, contains all the catchments
    """

    def __init__(self, N,low,medium,high):
        """
        Initialise the map matrix 'm'. And store colour values.

        Input:
            N = amount of rows of hydrated land on either side of the river
            high, medium, low = amount of water rows with that water-intensity (per side; its symmetric as of now)

        """
        # Set indices as matrix entries to distinguish from hydrated soil while colouring
        self.farmer_index = 100 
        self.water_index = 10

        """Set amount of water rows and check, that amount of rows is feasable"""
        water = 1 #N - 2*high - 2*medium - 2*low #<- alternative for wider rivers and matching dimensions
        self.m = np.ones((N+water, N))     # generate matrix
        assert(2*(high + medium + low) == N)   

        """ These lists have corresponding entries: name (for legend), amount of rows, colour and index"""
        self._plot_names = ["Low Hydration", "Medium Hydration", "High Hydration", "River", "Farmer"]
        self.amounts = [low,medium,high,water] # list of integers :)
        self.colours = ["#d16654","#bf9952", "#71B48D","#4170ba",'#e01fda'] # (left to right: red, orange, green, blue, farmercolour)
        self.weights = [0.25,0.5, 1,self.water_index,self.farmer_index,self.farmer_index+1]

        print('Done: Initialised map.')


    def generateMap(self):
        """
        Generate the basic map entries based on the specified amounts of water.
        """

        row = 0

        """  Set matrix (m) entries as specified """
        for index, amount in enumerate(self.amounts): 
            for _ in range(amount):
                self.m[row,:] = self.weights[index]
                self.m[-(row+1),:] = self.weights[index] # based on symmetry color two at once
                row += 1
        
        self.reference = np.copy(self.m)    # just so that the initial map is not destroyed by adding farmers; this matrix should never be modified
        print(self.reference)               # to check that the generation was succesful 
        print('Done: Generated map.')

        # Depreciated: (according to Aaron)
        """ 
        for i, j in product(range(N), repeat=2):
            if 0.5 + 1 / N > (i / N) > 0.5 - 1 / N:
                m[i, j] = 0.0
            if 0.75 <= (i / N) or (i / N) <= 0.25:
                m[i, j] = 0.5 
        """

    def reset_map(self):
        """ Used to reset the active matrix (m) back to the reference. """
        self.m = np.copy(self.reference)

    def add_farmers(self,pos_list):
        """ Add locations of farmer into the map 
        
        Input:
        - pos_list = List of (2-dim) tuples of the farmer position
        """
        self.reset_map()    # get a clear starting point
        
        # TODO all this could probably be optimised using the "GridIter" or "attrField" 
        for pos in pos_list:
            self.m[pos] = self.farmer_index # overwrite index of farmers
        
        print(f"Done: added {len(pos_list)} farmers onto map.")

    def show(self):
        """
        Show the map in colours
        """
        # Generate Matplotlib figure
        fig = plt.figure()
        ax = plt.subplot(111) # idk why 111, recommended in source
        plt.tight_layout(rect=[0,0,0.75,1]) #dont know if necessary
        plt.title("CropWar - Map")


        """ Generate Patches for nice plot legends"""
        #source: https://moonbooks.org/Articles/How-to-manually-add-a-legend-with-a-color-box-on-a-matplotlib-figure-/"""
        legend_patches = []
        for i, _label in enumerate(self._plot_names):
            _patch = mpatches.Patch(color = self.colours[i], label = _label)
            legend_patches.append(_patch)
        print(legend_patches)
        
        # Formatting source:https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height*0.9])
        plt.legend(handles=legend_patches,bbox_to_anchor=(1.04,0.5), loc="center left",
                 fancybox=True, shadow=True, ncol=1)
    
        crop_cmap, crop_norm = colors.from_levels_and_colors(self.weights, self.colours)
        ax.pcolormesh(self.m, cmap=crop_cmap, norm=crop_norm, edgecolors='k')

        ax = plt.gca()
        ax.set_aspect('equal')
        plt.show()