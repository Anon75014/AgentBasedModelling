""" File contains the Map class, to generate and display the CropWar map. """

import os
from copy import deepcopy

import matplotlib._color_data as mcd
import matplotlib.patches as mpatches  # used for legend in plt plot
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image
from matplotlib.colors import from_levels_and_colors


class map_class:
    """This class is used to visualise the spatial map of CropWar.
    """
    def __init__(self, _model):
        """Initialise Visualisation Class.

        Assumptions: Hydration levels are:low = 0.25, medium = 0.5, high = 1, water index = 10
        :param _model: the CropWar model at a certain time
        :type _model: ap.model (agentpy model)
        """

        self.model = _model
        self.water_matrix = self.model.grid.attr_grid("water")

        """ These lists have corresponding entries:
        name (for legend), amount of rows, colour and index"""
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

    def initialise_farmers(self):
        """Assign colours and modify colourlimits.
        """
        for farmer in self.model.farmers:
            color_list = [
            "#F28D11",
            "#0E5DE8",
            "#2BD941",
            "#D41717",
        ] # (left to right: orange, blue, green, red)
            _color = color_list[farmer.id-44] #farmer ID starts at 44
            self.colours.append(_color)
            self.weights.append(farmer.id)
            self._plot_names.append(f"Farmer {farmer.id}")

        self.weights.append(self.weights[-1] * 2)  # needed in "from_levels..."

        print("Done: initialised farmer in map_class.")

    def place_farmers(self):
        """Add locations of farmer into the map.
        :"""

        """ Modify the watermap by replaciing entries with farmer_id """
        _raw_id_matrix = np.array(self.model.grid.attr_grid("farmer_id"))
        _combined_matrix = deepcopy(np.array(self.water_matrix))
        # using 'putmask' we can change the entries according to a condition
        np.putmask(_combined_matrix, _raw_id_matrix > 0, _raw_id_matrix)
        self.processed_matrix = _combined_matrix
        print("Done: updated farmers in map_class.")

    def show(self, return_img=False):
        """Show the map in colours.

        :param return_img: [description], defaults to False
        :type return_img: bool, optional
        :return: the PIL image at the current time step
        :rtype: PIL.image
        """        
        # Generate Matplotlib figure
        fig = plt.figure()
        ax = plt.subplot(111)  # idk why 111, recommended in source
        plt.tight_layout(rect=[0, 0, 0.75, 1])  # dont know if necessary
        plt.title("CropWar - Map")

        # Generate patches for nice plot legends
        # source: https://moonbooks.org/Articles/
        # How-to-manually-add-a-legend-with-a-color-box-on-a-matplotlib-figure-/"""
        legend_patches = []
        for i, _label in enumerate(self._plot_names):
            _patch = mpatches.Patch(color=self.colours[i], label=_label)
            legend_patches.append(_patch)

        # print(legend_patches)

        # Formatting source:https://stackoverflow.com/questions/4700614/
        # how-to-put-the-legend-out-of-the-plot
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

        # source for "from_levels..." https://stackoverflow.com/questions/
        # 32769706/how-to-define-colormap-with-absolute-values-with-matplotlib
        crop_cmap, crop_norm = from_levels_and_colors(self.weights, self.colours)
        ax.pcolormesh(
            self.processed_matrix, cmap=crop_cmap, norm=crop_norm, edgecolors="k"
        )

        ax = plt.gca()
        ax.set_aspect("equal")

        if return_img:
            fig = plt.gcf()
            # {self.model.t}.png")
            dirname = os.path.dirname(os.path.abspath(__file__))
            filename = dirname + "/images/final_map.png"
            fig.savefig(filename)
            img =  PIL.Image.frombytes(
                "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
            )
            plt.close()
            return img
        else:
            plt.show()

        # TODO : Idea put crop numbers or so inside of patches...
