""" This File contains all the information to the crops awailable in CropWar. """


class Crop:
    """
    Crop super class
    """

    def __init__(self, _ID, _seed_cost=0, _sell_price=0, _harvest_yield=0):
        # Properties that every Crop must have
        self.ID = _ID  # basically its name, used to distinct in arrays, plots etc
        self.seed_cost = _seed_cost  # cost for a farmer to change crops
        self.sell_price = _sell_price  # price at which a unit (1) crop can be sold. TODO: vary prices with market
        self.harvest_yield = _harvest_yield  # amount of units a harvest will yield


class Crop_sortiment:
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

        ID = self.total_amount  # assign new ID
        self.total_amount += 1  # now there is one more

        # generate new Crop-instance based on Crop-class and add to dict:
        self.crops[ID] = Crop(ID, seed_cost, sell_price, harvest_yield)
        print(f"Done: added Crop{ID} to sortiment.")


# The Crop_Shop contains the relevant information for the farmers.
Crop_Shop = Crop_sortiment()
Crop_Shop.add_crop(100, 15, 2)  # Add two crops TODO Find good parameters for crops.
Crop_Shop.add_crop(150, 25, 1)
