import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from matplotlib import cm
from matplotlib.colors import ListedColormap

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
    def __init__(self):
        pass

    def show(self):
        """
        Show the map
        """
        # First experiment with drawing a simple map
        cmap = ListedColormap(["#7EBCE6", "#DBBEA1", "#71B48D"])
        N = 10
        m = np.ones((10, 10))
        for i, j in product(range(N), repeat=2):
            if 0.5 + 1 / N > (i / N) > 0.5 - 1 / N:
                m[i, j] = 0.0
            if 0.75 <= (i / N) or (i / N) <= 0.25:
                m[i, j] = 0.5
        plt.figure()
        plt.pcolormesh(m, cmap=cmap, edgecolors='k')
        ax = plt.gca()
        ax.set_aspect('equal')
        plt.show()
