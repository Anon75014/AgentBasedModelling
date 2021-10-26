import agentpy as ap

from enum import Enum, auto


class Personality(Enum):  # TODO Implenent Personalities
    """
    Personalities of the Farmers
    Maybe use Strategy design pattern for this?
    
    --> Each personality refers to a certain strategy interaction for the market or expansion (to be implemented).
    """

    Stocker = auto()
    Seller = auto()
    Pioneer = auto()  # Strategy: decide whether to invest in seeds and harvest next period or to invest in land and harvest then. 
    Efficiency = auto()  # Strategy: decide whether to invest in seeds and harvest or to invest in technology and thereby increase harvest_yield for all crops


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
            0, len(self.model.crop_shop.crops) - 1
        )  # -1 since len is  >= 1 and crop id starts at 0
        self.choose_crop(self.crop_id)

        # Initialise Stock
        self.stock = {}
        for crop_id in self.model.crop_shop.crops.keys():
            self.stock[crop_id] = 0

    def choose_crop(self, new_id: int):
        self.crop_id = new_id
        self.crop = self.model.crop_shop.crops[new_id]
        self.budget -= self.crop.seed_cost
        print(
            f"Farmer {self.id} changed crop to {self.crop_id}. New Budget: {self.budget}"
        )

    def farm(self):
        self.stock[self.crop_id] += self.crop.harvest_yield
        print(f"Farmer {self.id} harvested. New Stock: {self.stock}")

    def sell(self, crop_id: int, amount: int):
        if self.stock[crop_id] >= amount:
            self.stock[crop_id] -= amount
            self.budget += self.crop.sell_price
            print(
                f"Farmer {self.id} Sold. New Stock: {self.stock}. New Budget: {self.budget}"
            )
        else:
            print(
                f"ERROR: Farmer {self.id} does not have enough in stock for that deal."
            )
