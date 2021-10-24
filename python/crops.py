"""
Contains all the information about the crops available in CropWar.
"""

class Crop:
    """
    Crop super class
    """

    def __init__(self, crop_id, seed_cost=0, sell_price=0, harvest_yield=0):
        # Properties that every Crop must have
        self.crop_id = crop_id  # basically its name, used to distinct in arrays, plots etc
        self.seed_cost = seed_cost  # cost for a farmer to change crops
        self.sell_price = sell_price  # price at which a unit (1) crop can be sold. TODO: vary prices with market
        self.harvest_yield = harvest_yield  # amount of units a harvest will yield


class CropSortiment:
    """
    Class for crop interaction and tracking
    """

    def __init__(self):
        """Initialise the crop sortiment"""
        self.total_amount = (
            0  # number of available crops; to track and for ID-assignement
        )
        self.crops = {}  # dictionary of available crops
        print("Done: Created Crop_sortiment instance.")

    def add_crop(self, seed_cost, sell_price, harvest_yield):
        """Add a new kind of Crop to the sortiment"""

        crop_id = self.total_amount  # assign new ID
        self.total_amount += 1  # now there is one more

        # generate new Crop-instance based on Crop-class and add to dict:
        self.crops[crop_id] = Crop(crop_id, seed_cost, sell_price, harvest_yield)
        print(f"Done: added Crop{crop_id} to sortiment.")


