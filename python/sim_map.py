""" This file contains the Map class, designed to generate and display the CropWar map. """

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches  # used for legend in plt plot
from typing import List, Tuple


class Map:
    """
    Entire map, contains all the catchments
    """

    def __init__(self, low: int, medium: int, high: int):
        """
        Initialise the map matrix 'm'. And store colour values.

        Parameters
        ----------
        high, medium, low: int
            Amount of water rows with that water-intensity (per side; its symmetric as of now)

        Ideas:
            - alternative for wider rivers and matching dimensions: water = n_land_rows - 2*high - 2*medium - 2*low
        """
        # Set indices as matrix entries to distinguish from hydrated soil while colouring
        self.farmer_index = 100
        self.water_index = 10

        """Set amount of water rows and check, that amount of rows is feasable"""
        n_land_rows = 2 * (low + medium + high)
        water = 1
        self.map_matrix = np.ones((n_land_rows + water, n_land_rows))  # generate matrix

        """ These lists have corresponding entries: name (for legend), amount of rows, colour and index"""
        self._plot_names = [
            "Low Hydration",
            "Medium Hydration",
            "High Hydration",
            "River",
            "Farmer",
        ]
        self.amounts = [low, medium, high, water]  # list of integers :)
        self.colours = [
            "#d16654",
            "#bf9952",
            "#71B48D",
            "#4170ba",
            "#e01fda",
        ]  # (left to right: red, orange, green, blue, farmercolour)
        self.weights = [
            0.25,
            0.5,
            1,
            self.water_index,
            self.farmer_index,
            self.farmer_index + 1,
        ]

        print("Done: Initialised map.")

    def generate_map(self):
        """
        Generate the basic map entries based on the specified amounts of water.
        """

        row = 0

        """  Set matrix (m) entries as specified """
        for index, amount in enumerate(self.amounts):
            for _ in range(amount):
                  # based on symmetry color two at once
                self.map_matrix[row, :] = self.weights[index]
                self.map_matrix[-(row + 1), :] = self.weights[index]
                row += 1

        self.reference = np.copy(
            self.map_matrix
        )  # just so that the initial map is not destroyed by adding farmers; this matrix should never be modified
        # Aaron: I think we can also just color over the map at the farmer positions instead of copying the entire map
        print(self.reference)  # to check that the generation was succesful
        print("Done: Generated map.")

    def reset_map(self):
        """Used to reset the active matrix (m) back to the reference."""
        self.map_matrix = np.copy(self.reference)

    def add_farmers(self, pos_list: List[Tuple[int, int]]):
        """Add locations of farmer into the map

        Parameters
        ----------
        pos_list: List[Tuple[int, int]]
            List of (2-dim) tuples of the farmer position
        """
        self.reset_map()  # get a clear starting point

        # TODO all this could probably be optimised using the "GridIter" or "attrField"
        for pos in pos_list:
            self.map_matrix[pos] = self.farmer_index  # overwrite index of farmers

        print(f"Done: added {len(pos_list)} farmers onto map.")

    def show(self):
        """
        Show the map in colours
        """
        # Generate Matplotlib figure
        fig = plt.figure()
        ax = plt.subplot(111)  # idk why 111, recommended in source
        plt.tight_layout(rect=[0, 0, 0.75, 1])  # dont know if necessary
        plt.title("CropWar - Map")

        # Generate patches for nice plot legends
        # source: https://moonbooks.org/Articles/How-to-manually-add-a-legend-with-a-color-box-on-a-matplotlib-figure-/"""
        legend_patches = []
        for i, _label in enumerate(self._plot_names):
            _patch = mpatches.Patch(color=self.colours[i], label=_label)
            legend_patches.append(_patch)
        print(legend_patches)

        # Formatting source:https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.9])
        plt.legend(
            handles=legend_patches,
            bbox_to_anchor=(1.04, 0.5),
            loc="center left",
            fancybox=True,
            shadow=True,
            ncol=1,
        )

        # source for "from_levels..." https://stackoverflow.com/questions/32769706/how-to-define-colormap-with-absolute-values-with-matplotlib
        crop_cmap, crop_norm = colors.from_levels_and_colors(self.weights, self.colours)
        ax.pcolormesh(self.map_matrix, cmap=crop_cmap, norm=crop_norm, edgecolors="k")

        ax = plt.gca()
        ax.set_aspect("equal")
        plt.show()

        # TODO : Idea put crop numbers or so inside of patches...


class Catchment:
    """
    Catchments in which the farmers will compete
    """

    def __init__(self):
        pass
        #       source: https://stackoverflow.com/questions/20998083/show-the-values-in-the-grid-using-matplotlib
