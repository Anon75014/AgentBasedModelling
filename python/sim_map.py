import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from matplotlib import cm
import matplotlib.colors as colors
from math import ceil
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
            N = amount of lines of water
            high, medium, low = amount of water rows with that water-intensity
        
        """
        water = N - 2*high - 2*medium - 2*low
        self.m = np.ones((N, N-water))

        self.amounts = [low,medium,high,water]
        self.colours = ["#d16654","#bf9952", "#71B48D","#4170ba"] # (left to right: red, orange, green, blue)
        self.weights = [0.25,0.5, 1, 10,11]

        print('Done: Initialised map.')

    def generateMap(self):
        """
        Generate the Map entries based on the specified amounts of Water.
        """
        row = 0

        for index, amount in enumerate(self.amounts): # colour each row
            for _ in range(amount):
                self.m[row,:] = self.weights[index]
                self.m[-(row+1),:] = self.weights[index] # based on symmetry color two at once
                row += 1
        
        print(self.m)    
        print('Done: Generated map.')

        # Alternatively
        """ 
        for i, j in product(range(N), repeat=2):
            if 0.5 + 1 / N > (i / N) > 0.5 - 1 / N:
                m[i, j] = 0.0
            if 0.75 <= (i / N) or (i / N) <= 0.25:
                m[i, j] = 0.5 
        """

    def show(self):
        """
        Show the map
        """
        pass
        
        
        # Generate Matplotlib figure
        plt.figure()
        crop_cmap, crop_norm = colors.from_levels_and_colors(self.weights, self.colours)
        plt.pcolormesh(self.m, cmap=crop_cmap, norm=crop_norm, edgecolors='k')
        ax = plt.gca()
        ax.set_aspect('equal')
        plt.show()