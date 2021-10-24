import agentpy as ap
from crops import Crop_Shop

from enum import Enum, auto


class Personality(Enum):  # TODO Implenent Personalities
    """
    Personalities of the Farmers
    Maybe use Strategy design pattern for this?
    """

    Stocker = auto()
    Seller = auto()


class Farmer(ap.Agent):
    def setup(self):
        """Initiate agent attributes."""
        self.grid = self.model.grid
        self.random = self.model.random

        # Set start budget
        self.budget = self.p.start_budget

        # self.field_locations = np.zeros(shape=(2,1)) # list where subfield locations are stored

        # Set start crop
        self.crop = None
        self.crop_id = self.random.randint(
            0, len(Crop_Shop.crops) - 1
        )  # -1 since len is  >= 1 and crop id starts at 0
        self.choose_crop(self.crop_id)

        # Initialise Stock
        self.stock = {}
        for _crop_id in Crop_Shop.crops.keys():
            self.stock[_crop_id] = 0

    def choose_crop(self, new_id):
        self.crop_id = new_id
        self.crop = Crop_Shop.crops[new_id]
        self.budget -= self.crop.seed_cost
        print(
            f"Farmer {self.id} changed crop to {self.crop_id}. New Budget: {self.budget}"
        )

    def farm(self):
        self.stock[self.crop_id] += self.crop.harvest_yield
        print(f"Farmer {self.id} harvested. New Stock: {self.stock}")

    def sell(self, _id, _amount):
        if self.stock[_id] >= _amount:
            self.stock[_id] -= _amount
            self.budget += self.crop.sell_price
            print(
                f"Farmer {self.id} Sold. New Stock: {self.stock}. New Budget: {self.budget}"
            )
        else:
            print(
                f"ERROR: Farmer {self.id} does not have enough in stock for that deal."
            )


''' Somewhat depreciated with the use of AgentPy
class Farmer:
    """
    Farmer agent
    """
    def __init__(self,
                 position: np.ndarray,
                 pers: Personality,
                 catchment: Catchment):
        """
        Parameters
        ----------
        position : np.ndarray
            position on the map
        pers: enum.Personality
            Personality of the agent
        catchment: Catchment
            Catchment in which the farmer will compete
        """
        pass

 '''
