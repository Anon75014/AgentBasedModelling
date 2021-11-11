from crops import CropSortiment
import numpy as np
import agentpy as ap
from dataclasses import dataclass
from typing import Dict, Optional


class Market:
    """
    Market which regulates the prices of the crops
    """
    def __init__(self, crop_sortiment: CropSortiment, agents: ap.AgentList) -> None:
        self.crop_sortiment = crop_sortiment
        self.agents = agents
        self.current_demand : Dict[int, int] = {k: 5 for k in crop_sortiment.crops.keys()}
        self.current_stock : Dict[int, int] = {k: 0 for k in crop_sortiment.crops.keys()}
        self.current_supply : Dict[int, int] = {k: 0 for k in crop_sortiment.crops.keys()}
        self.current_prices : Dict[int, int] = {k: 0 for k in crop_sortiment.crops.keys()}
        self.MAX_PRICE = 1e6

    def _calc_current_demand(self) -> None:
        """
        Calculates the current demand
        """
        self.current_demand = {k: 10 for k in self.crop_sortiment.crops.keys()}

    def _calc_global_stock(self) -> None:
        """
        Calculates all the available resources
        """
        self.current_stock = {k: 0 for k in self.crop_sortiment.crops.keys()}
        for agent in self.agents:
            for crop_id, crop_stock in agent.stock.items():
                self.current_stock[crop_id] += crop_stock
        print("Global stock is {}".format(self.current_stock))

    def calc_global_price(self) -> np.ndarray:
        self._calc_current_demand()
        self._calc_global_stock()
        global_prices: Dict[int, float] = self.current_demand
        for crop_id, crop_demand in global_prices.items():
            r = np.random.random() # Random component of the demand
            if self.current_stock[crop_id] != 0:
                global_prices[crop_id] = np.max(
                [(
                    self.crop_sortiment.crops[crop_id].sell_price # Current crop price
                    * (crop_demand + r)
                    / self.current_stock[crop_id]
                ), self.MAX_PRICE])
            else:
                global_prices[crop_id] = self.MAX_PRICE
        self.current_prices = global_prices
        return global_prices

    def calc_global_supply(self) -> np.ndarray:
        self.calc_global_price()
        self.current_supply = {k: 0 for k in self.crop_sortiment.crops.keys()}
        for agent in self.agents:
            supply_from_agent = agent.supply(self.current_prices)
            for crop_id in self.current_supply.keys():
                self.current_supply[crop_id] += supply_from_agent[crop_id]
        return self.current_supply

    def step(self):
        prices = self.calc_global_price()
        supp = self.calc_global_supply()
        print(f"Market: Global supply is {supp} at prices {prices}")
