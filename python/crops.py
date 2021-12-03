"""
Contains all the information about the crops available in CropWar.
"""
from typing import Optional, List
from itertools import combinations
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Crop:
    """Crop Super Class"""

    def __init__(
        self,
        crop_id: int,
        seed_cost: float = 0.0,
        sell_price: float = 0.0,
        max_harvest_yield: float = 0.0,
        water_need: float = 0.0,
        crop_factor: Optional[List[float]] = None,
        k_c_y: Optional[float] = None,
        manure_need: Optional[float] = None,
        phosphorus_need: Optional[float] = None,
        potassium_need: Optional[float] = None,
        nitrogen_need: Optional[float] = None,
        herbicide_need: Optional[float] = None,
        insecticide_need: Optional[float] = None,
        fungicide_need: Optional[float] = None,
        labor_need: Optional[float] = None,
        machinery_hour: Optional[float] = None,
    ):
        """Properties that every Crop must have

        :param crop_id: ID used to distinguish
        :type crop_id: int
        :param seed_cost: Cost to buy seed for a single Cell, defaults to 0
        :type seed_cost: float, optional
        :param sell_price: Sell price per unit, defaults to 0
        :type sell_price: float, optional
        :param harvest_yield: [description], defaults to 0
        :type harvest_yield: float, optional
        :param water_need: [description], defaults to 0.0
        :type water_need: float, optional
        :yield: [description]
        :rtype: [type]
        """
        # basically its name, used to distinct in arrays, plots etc ::
        self._id = crop_id
        self.water_need = water_need
        self.seed_cost = seed_cost  # cost for a farmer to change crops
        self.sell_price = sell_price  # price at which a unit (1) crop can be sold. TODO: vary prices with market
        self.base_price = sell_price
        self.max_harvest_yield = max_harvest_yield  # amount of units a harvest will yield
        self.crop_factor = crop_factor
        self.k_c_y = k_c_y
        self.manure_need = manure_need
        self.phosphorus_need = phosphorus_need
        self.potassium_need = potassium_need
        self.nitrogen_need = nitrogen_need
        self.herbicide_need = herbicide_need
        self.insecticide_need = insecticide_need
        self.fungicide_need = fungicide_need
        self.labor_need = labor_need
        self.machinery_hour = machinery_hour

    def change_crop_id(self, new_id: int):
        self._id = new_id

    def get_harvest_yield(self, di: float) -> List[float]:
        s = 0.0
        for j, k_c_y in enumerate(self.k_c_y):
            s += k_c_y * (1.0 - (di / (self.crop_factor[j])))
        harvest_yield = np.max([self.max_harvest_yield * (1.0 - s), 0.0])
        return harvest_yield

    def _get_gwp(self, area):
        # TODO: Make actually work
        #Area must be in ha
        GWP_fertilizer = [(
            self.manure_need[i] * 8.96384
            + self.phosphorus_need[i] * 1.5
            + self.potassium_need[i] * 0.98
            + self.nitrogen_need[i] * 8.3
        ) * area[i] for i in range(len(area))]
        GWP_biocide = [(
            self.herbicide_need[i] * 6.3 + self.insecticide_need[i] * 5.1 + self.fungicide_need[i] * 3.9
        ) * area[i] for i in range(len(area))]
        GWP_machinery = [93.38 * self.machinery_hour[i] * 2.6845 * 0.071 * area[i] for i in range(len(area))]
        GWP_fuel = [self.machinery_hour[i] * 17.81 * 2.347 * area[i] for i in range(len(area))]
        GWP_electricity = [self.water_need[i] * 10 * 0.2323 * 0.608 for i in range(len(area))]
        GWP_total = [(
            GWP_fertilizer[i]
            + GWP_biocide[i]
            + GWP_machinery[i]
            + GWP_fuel[i]
            + GWP_electricity[i]
        ) for i in range(len(area))]
        return GWP_total

    def _info_dict(self) -> dict:
        """Used to generate a dict so that the config can be saved into a json file.

        :return: Information packed dictionary
        :rtype: dict
        """
        crop_variables = [
            attr
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__")
        ]
        info_dict = {var: self.__getattribute__(var) for var in crop_variables}
        return info_dict

class CropSortiment:
    """Class for crop interaction and tracking"""

    def __init__(self):
        """Initialise the crop sortiment"""
        # number of available crops; to track and for ID-assignement
        self.amount_of_crops = 0
        self.crops = {}
        # print("Done: Created Crop_sortiment instance.")

    def add_crop(self, seed_cost: float, sell_price: float, max_harvest_yield: float, water_need: float):
        """Add a new kind of Crop to the sortiment

        :param area: [description]
        :type area: float
        :param crop_type: [description]
        :type crop_type: float
        :param di: [description]
        :type di: float
        """
        crop_id = self.amount_of_crops
        self.amount_of_crops += 1
        # generate new Crop-instance based on Crop-class and add to dict:
        self.crops[crop_id] = Crop(crop_id, seed_cost, sell_price, max_harvest_yield, water_need)
        # print(f"Done: added Crop{crop_id} to sortiment.")

    def add_crop(self, new_crop: Crop):
        crop_id = self.amount_of_crops
        self.amount_of_crops += 1
        new_crop.change_crop_id(crop_id)
        self.crops[crop_id] = new_crop

    def _info_dict(self) -> dict:
        """Reformat for storage in config_file

        :return: Information packed dictionary
        :rtype: dict
        """
        cropshop_dict = {crop._id: crop._info_dict() for crop in self.crops.values()}
        return cropshop_dict

WinterWheat = Crop(
    crop_id=1,
    seed_cost=84.03,
    sell_price=0.125,
    max_harvest_yield=7.0,
    water_need=1.0,
    crop_factor=[0.6, 1.2, 0.75, 0.25],
    k_c_y=[0.2, 0.6, 0.5, 0.4],
    manure_need=0.0,
    phosphorus_need=89.96,
    potassium_need=200.06,
    nitrogen_need=29.99,
    herbicide_need=630.0,
    insecticide_need=100.0,
    fungicide_need=10.0,
    labor_need=3.67,
    machinery_hour=18.5,
)

Barley = Crop(
    crop_id=2,
    seed_cost=61.60,
    sell_price=0.074,
    max_harvest_yield=4.7,
    water_need=1.0,
    crop_factor=[0.8, 1.0, 1.05, 0.4],
    k_c_y=[0.2, 0.6, 0.5, 0.4],
    manure_need=0.0,
    phosphorus_need=18.72,
    potassium_need=102.87,
    nitrogen_need=17.32,
    herbicide_need=630.0,
    insecticide_need=10.0,
    fungicide_need=0.0,
    labor_need=5.46,
    machinery_hour=18.5,
)

Maize = Crop(
    crop_id=3,
    seed_cost=142.06,
    sell_price=0.077,
    max_harvest_yield=10.0,
    water_need=1.0,
    crop_factor=[0.7, 1.2, 1.15, 1.1],
    k_c_y=[0.4, 1.5, 0.5, 0.2],
    manure_need=0.0,
    phosphorus_need=136.66,
    potassium_need=39.0,
    nitrogen_need=246.85,
    herbicide_need=230.0,
    insecticide_need=0.0,
    fungicide_need=30.0,
    labor_need=6.14,
    machinery_hour=19.0,
)

Beans = Crop(
    crop_id=4,
    seed_cost=156.43,
    sell_price=0.2146,
    max_harvest_yield=12.0,
    water_need=1.0,
    crop_factor=[0.6, 1.2, 0.75, 0.3],
    k_c_y=[0.2, 1.1, 0.75, 0.2],
    manure_need=0.0,
    phosphorus_need=93.33,
    potassium_need=0.0,
    nitrogen_need=186.66,
    herbicide_need=660.0,
    insecticide_need=0.0,
    fungicide_need=0.0,
    labor_need=8.62,
    machinery_hour=16.0,
)

Cucumbers = Crop(
    crop_id=5,
    seed_cost=240.11,
    sell_price=0.065,
    max_harvest_yield=25.0,
    water_need=1.0,
    crop_factor=[0.5, 1.0, 0.80],
    k_c_y=[0.84, 0.84, 0.84],
    manure_need=3500.0,
    phosphorus_need=125.54,
    potassium_need=72.99,
    nitrogen_need=210.06,
    herbicide_need=0.0,
    insecticide_need=880.0,
    fungicide_need=1030.0,
    labor_need=34.53,
    machinery_hour=22.5,
)

Tomatoes = Crop(
    crop_id=6,
    seed_cost=292.44,
    sell_price=0.052,
    max_harvest_yield=35.0,
    water_need=1.0,
    crop_factor=[0.65, 1.25, 0.95, 0.65],
    k_c_y=[0.4, 1.1, 0.8, 0.4],
    manure_need=3400.0,
    phosphorus_need=86.45,
    potassium_need=43.22,
    nitrogen_need=177.23,
    herbicide_need=1200.0,
    insecticide_need=1040.0,
    fungicide_need=900.0,
    labor_need=28.05,
    machinery_hour=22.5,
)

Watermelons = Crop(
    crop_id=7,
    seed_cost=208.96,
    sell_price=0.028,
    max_harvest_yield=40.0,
    water_need=1.0,
    crop_factor=[0.65, 1.05, 0.9, 0.75],
    k_c_y=[0.45, 0.7, 0.8, 0.8],
    manure_need=2800.0,
    phosphorus_need=109.77,
    potassium_need=59.01,
    nitrogen_need=201.76,
    herbicide_need=1190.0,
    insecticide_need=1020.0,
    fungicide_need=700.0,
    labor_need=13.79,
    machinery_hour=22.5,
)

Alfalfa = Crop(
    crop_id=8,
    seed_cost=101.47,
    sell_price=0.81,
    max_harvest_yield=3.5,
    water_need=1.0,
    crop_factor=[0.4, 1.2],
    k_c_y=[1.1, 1.1],
    manure_need=2200.0,
    phosphorus_need=198.57,
    potassium_need=14.28,
    nitrogen_need=13.56,
    herbicide_need=1280.0,
    insecticide_need=120.0,
    fungicide_need=50.0,
    labor_need=11.31,
    machinery_hour=19.0,
)

Sorghum = Crop(
    crop_id=9,
    seed_cost=150.67,
    sell_price=0.063,
    max_harvest_yield=8.0,
    water_need=1.0,
    crop_factor=[0.575, 1.15, 0.8, 0.55],
    k_c_y=[0.2, 0.55, 0.45, 0.20],
    manure_need=1000.0,
    phosphorus_need=91.14,
    potassium_need=11.47,
    nitrogen_need=393.59,
    herbicide_need=160.0,
    insecticide_need=480.0,
    fungicide_need=0.0,
    labor_need=4.48,
    machinery_hour=19.0,
)

Rapeseed = Crop(
    crop_id=10,
    seed_cost=81.03,
    sell_price=0.088,
    max_harvest_yield=4.0,
    water_need=1.0,
    crop_factor=[0.35, 1.15, 0.35],
    k_c_y=[0.87, 0.87, 0.87],
    manure_need=0.0,
    phosphorus_need=73.65,
    potassium_need=20.94,
    nitrogen_need=232.62,
    herbicide_need=2560.0,
    insecticide_need=630.0,
    fungicide_need=120.0,
    labor_need=2.65,
    machinery_hour=0.0,
)

if __name__ == "__main__":
    crop_shop = CropSortiment()
    crop_shop.add_crop(1, 1, 1)  # area, crop_type, available water
    crop_shop.add_crop(1, 9, 1)
    pass
