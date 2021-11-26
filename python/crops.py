"""
Contains all the information about the crops available in CropWar.
"""
#%%
import crop_model as cm


class CropSortiment:
    """
    Class for crop interaction and tracking
    """

    def __init__(self):
        """Initialise the crop sortiment"""
        # number of available crops; to track and for ID-assignement
        self.amount_of_crops = 0
        self.crops = {}
        # print("Done: Created Crop_sortiment instance.")

    def crop_yield(self, area: float, crop_type: float, di: float):
        y_c_a, cost, income = cm.agr(area, crop_type, di)

    # def add_crop(self, seed_cost: float, sell_price: float, harvest_yield: float):
    def add_crop(self, area: float, crop_type: float, di: float):
        """Add a new kind of Crop to the sortiment"""

        crop_id = self.amount_of_crops
        self.amount_of_crops += 1
        harvest_yield, seed_cost, sell_price = cm.agr(area, crop_type, di)
        # generate new Crop-instance based on Crop-class and add to dict:
        # Aaron: Maybe better to add crop instances instead of creating them in here.
        self.crops[crop_id] = Crop(crop_id, seed_cost, sell_price, harvest_yield, 1.0)
        # print(f"Done: added Crop{crop_id} to sortiment.")

    def _info_dict(self) -> dict:
        """Reformat for storage in config_file"""
        cropshop_dict = {crop._id: crop._info_dict() for crop in self.crops.values()}
        return cropshop_dict


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
        water_need: float = 0.0
    ):
        """Properties that every Crop must have"""
        # basically its name, used to distinct in arrays, plots etc ::
        self._id = crop_id
        self.water_need = water_need
        self.seed_cost = seed_cost  # cost for a farmer to change crops
        self.sell_price = sell_price  # price at which a unit (1) crop can be sold. TODO: vary prices with market
        self.harvest_yield = harvest_yield  # amount of units a harvest will yield

    def _info_dict(self) -> dict:
        """Used to generate a dict so that the config can be saved into a json file."""
        crop_variables  = [
            attr
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__")
        ]
        info_dict = {var:self.__getattribute__(var) for var in crop_variables}
        return info_dict


if __name__ == '__main__':
    crop_shop = CropSortiment()
    crop_shop.add_crop(1, 1, 1)  # area, crop_type, available water
    crop_shop.add_crop(1, 9, 1)
    pass
# %%
