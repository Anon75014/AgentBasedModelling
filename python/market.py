from crops import CropSortiment
import numpy as np
import agentpy as ap
from dataclasses import dataclass
from typing import Dict, Optional


class Market:
    """
    Market which regulates the prices of the crops
    """

    def __init__(self, crop_sortiment: CropSortiment, agents: ap.AgentList, base_demand: float, demand_fraction: float) -> None:
        """
        Market model

        Parameters
        ----------
        crop_sortiment: CropSortiment
            The CropSortiment that is used in the model
        agents: ap.AgentList
            List of agents that participate in the market
        base_demand: float
            Base line for the demand
        demand_fraction: float
            Expansion factor for the demand
        """
        self.crop_sortiment = crop_sortiment
        self.agents = agents
        self.base_demand = base_demand
        self.demand_fraction = demand_fraction

        self.current_demand: Dict[int, int] = {
            k: self.base_demand for k in crop_sortiment.crops.keys()
        }
        self.current_stock: Dict[int, int] = {k: 1.0 for k in crop_sortiment.crops.keys()} # Initialize to 1 for initial demand calculation
        self.current_supply: Dict[int, int] = {
            k: 0 for k in crop_sortiment.crops.keys()
        }
        self.current_prices: Dict[int, int] = {
            crop_id: crop.sell_price for (crop_id, crop) in crop_sortiment.crops.items()
        }
        self.MAX_PRICE = 1e5

    def _calc_current_demand(self) -> None:
        """
        Calculates the current demand using an expansive market model
        """
        self.current_demand = {
            crop_id: self.base_demand + self.demand_fraction * self.current_stock[crop_id]
            for crop_id in self.crop_sortiment.crops.keys()
        }

    def _calc_global_stock(self) -> None:
        """
        Calculates all the available resources
        """
        self.current_stock = {k: 0.0 for k in self.crop_sortiment.crops.keys()}
        for agent in self.agents:
            for crop_id, crop_stock in agent.stock.items():
                self.current_stock[crop_id] += crop_stock
        print("Global stock is {}".format(self.current_stock))

    def calc_global_price(self) -> Dict[int, float]:
        """
        Calculates the global price according to supply and demand
        """
        self._calc_current_demand()
        self._calc_global_stock()
        for crop_id, crop_demand in self.current_demand.items():
            if self.current_stock[crop_id] != 0.0:
                self.current_prices[crop_id] = np.min(
                    [
                        (
                            self.crop_sortiment.crops[
                                crop_id
                            ].sell_price  # Current crop price
                            * crop_demand
                            / self.current_stock[crop_id]
                        ),
                        self.MAX_PRICE,
                    ]
                )
            else:
                self.current_prices[crop_id] = self.MAX_PRICE
        return self.current_prices

    def calc_global_supply(self) -> Dict[int, float]:
        """
        Calculates the total supply that is provided by the agents
        """
        self.calc_global_price()
        self.current_supply = {k: 0.0 for k in self.crop_sortiment.crops.keys()}
        self.agents.calc_supply(self.current_prices)

        # Sum the supply of the agents
        for agent in self.agents:
            for crop_id in self.current_supply.keys():
                self.current_supply[crop_id] += agent.supply[crop_id]

        # Calculate the exact amount of supply for each farmer
        for crop_id, current_demand in self.current_demand.items():
            current_supply = self.current_supply[crop_id]
            # Correct for oversupply, i.e. each farmer only supplies the demand
            # if the total supply is larger than the demand
            correction_factor = np.min([current_demand / current_supply, 1.0])
            for agent in self.agents:
                supply_from_agent = agent.supply[crop_id]
                agent.sell(crop_id, correction_factor * supply_from_agent)

        return self.current_supply

    def step(self):
        prices = self.current_prices.copy()
        supp = self.calc_global_supply()
        print(f"Market: Global supply is {supp} at prices {prices}")
