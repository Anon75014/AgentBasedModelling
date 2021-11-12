""" This file contains the Map class, designed to generate and display the CropWar map. """

from copy import deepcopy

import matplotlib._color_data as mcd
import matplotlib.patches as mpatches  # used for legend in plt plot
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import from_levels_and_colors


class map_class:
    def __init__(self, _model):
        """
        Initialise Visualisation Class

        Assumptions:
        - low = 0.25, medium = 0.5, high = 1, water index = 10
        """

        self.model = _model
        self.water_matrix = self.model.grid.attr_grid("water")

        """ These lists have corresponding entries: name (for legend), amount of rows, colour and index"""
        self._plot_names = [
            "Low Hydration",
            "Medium Hydration",
            "High Hydration",
            "River",
        ]
        self.colours = [
            "#d16654",
            "#bf9952",
            "#71B48D",
            "#4170ba",
        ]  # (left to right: red, orange, green, blue)
        self.weights = [0.25, 0.5, 1, 10]

        print("Done: Initialised map_class.")

    def add_farmers(self):
        """Add locations of farmer into the map"""

        """ Modify the watermap by replaciing entries with farmer_id """
        _raw_id_matrix = np.array(self.model.grid.attr_grid("farmer_id"))
        _combined_matrix = deepcopy(np.array(self.water_matrix))
        # using 'putmask' we can change the entries according to a condition
        np.putmask(_combined_matrix, _raw_id_matrix > 0, _raw_id_matrix)
        self.processed_matrix = _combined_matrix

        """ Assign colours and modify colourlimits """
        for farmer in self.model.farmers:
            _color = self.model.random.choice(list(mcd.XKCD_COLORS.values()))
            self.colours.append(_color)
            self.weights.append(farmer.id)
            self._plot_names.append(f"Farmer {farmer.id}")

        self.weights.append(self.weights[-1] * 2)  # needed in "from_levels..."

        print(f"Done: added farmers onto map.")

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

        # print(legend_patches)

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
        crop_cmap, crop_norm = from_levels_and_colors(
            self.weights, self.colours)
        ax.pcolormesh(self.processed_matrix, cmap=crop_cmap,
                      norm=crop_norm, edgecolors="k")

        ax = plt.gca()
        ax.set_aspect("equal")
        plt.show()

        # TODO : Idea put crop numbers or so inside of patches...