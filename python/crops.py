"""
Contains all the information about the crops available in CropWar.
"""



class CropSortiment:
    """
    Class for crop interaction and tracking
    """

    def __init__(self):
        """Initialise the crop sortiment"""
        # number of available crops; to track and for ID-assignement
        self.amount_of_crops = 0
        self.crops = {}
        print("Done: Created Crop_sortiment instance.")

    def add_crop(self, seed_cost: float, sell_price: float, harvest_yield: float):
        """Add a new kind of Crop to the sortiment"""

        crop_id = self.amount_of_crops
        self.amount_of_crops += 1

        # generate new Crop-instance based on Crop-class and add to dict:
        # Aaron: Maybe better to add crop instances instead of creating them in here.
        self.crops[crop_id] = Crop(crop_id, seed_cost, sell_price, harvest_yield)
        print(f"Done: added Crop{crop_id} to sortiment.")

class Crop:
    """
    Crop super class
    """

    def __init__(
        self,
        crop_id: int,
        seed_cost: float = 0,
        sell_price: float = 0,
        harvest_yield: float = 0,
    ):
        """ Properties that every Crop must have """
        # basically its name, used to distinct in arrays, plots etc ::
        self._id = (crop_id)
        self.seed_cost = seed_cost  # cost for a farmer to change crops
        self.sell_price = sell_price  # price at which a unit (1) crop can be sold. TODO: vary prices with market
        self.harvest_yield = harvest_yield  # amount of units a harvest will yield
