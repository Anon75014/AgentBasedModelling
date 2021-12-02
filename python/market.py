from crops import CropSortiment
import numpy as np
import agentpy as ap
from dataclasses import dataclass
from typing import Dict, Optional


class Market:
    """
    Market which regulates the prices of the crops
    """

    def __init__(
        self,
        crop_sortiment: CropSortiment,
        agents: ap.AgentList,
        base_demand: float,
        demand_fraction: float,
        max_price: float,
    ) -> None:
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
        self.current_stock: Dict[int, int] = {
            k: 1.0 for k in crop_sortiment.crops.keys()
        }  # Initialize to 1 for initial demand calculation
        self.current_supply: Dict[int, int] = {
            k: 0.0 for k in crop_sortiment.crops.keys()
        }
        self.current_prices: Dict[int, int] = {
            crop_id: crop.sell_price for (crop_id, crop) in crop_sortiment.crops.items()
        }
        self.max_price = max_price

    def _calc_current_demand(self) -> None:
        """
        Calculates the current demand using an expansive market model, i.e. the demand increases every iteration by a fixed fraction of the total stock.
        """
        self.current_demand = {
            crop_id: self.base_demand
            + self.demand_fraction * self.current_stock[crop_id]
            for crop_id in self.crop_sortiment.crops.keys()
        }

    def _calc_global_stock(self) -> None:
        """
        Calculates all the available resources. Due to the assumption of symmetric information, the total stock will be aggregated
        by adding the individual stocks of every agent for a certain commodity.
        """
        self.current_stock = {k: 0.0 for k in self.crop_sortiment.crops.keys()}
        for agent in self.agents:
            for crop_id, crop_stock in agent._stock.items():
                self.current_stock[crop_id] += crop_stock

    def calc_global_price(self) -> Dict[int, float]:
        """
        Calculates the global price according to supply and demand
        """
        self._calc_global_stock()
        self._calc_current_demand()  # based on t-1 stock
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
                        self.max_price,
                    ]
                )
            else:
                self.current_prices[crop_id] = self.max_price
        return self.current_prices

    def market_interaction(self) -> Dict[int, float]:
        """
        Calculates the total supply that is provided by the agents. The agents act according to their specification, i.e. their supply function.
        """
        self.agents.calc_supply(self.current_prices)
        self.calc_global_price()
        self.current_supply = {k: 0.0 for k in self.crop_sortiment.crops.keys()}

        # Sum the supply of the agents
        for agent in self.agents:
            for crop_id in self.current_supply.keys():
                self.current_supply[crop_id] += agent.supply[crop_id]

        # Calculate the exact amount of supply for each farmer
        for crop_id, current_demand in self.current_demand.items():
            current_supply = self.current_supply[crop_id]
            # Correct for oversupply, i.e. each farmer only supplies the demand
            # if the total supply is larger than the demand
            correction_factor = 1.0
            if current_supply != 0.0:
                correction_factor = np.min([current_demand / current_supply, 1.0])

            for agent in self.agents:
                supply_from_agent = agent.supply[crop_id]
                agent.sell(crop_id, correction_factor * supply_from_agent)

        return self.current_supply

    def step(self):
        self.market_interaction()

        # Update prices of crops & get highest price
        for crop_id, price in self.current_prices.items():
            self.crop_sortiment.crops[crop_id].sell_price = price

        self.highest_price_id = max(
            self.current_prices, key=self.current_prices.get
        )
        self.highest_price = max(self.current_prices.values())
        self.crop_prices = self.current_prices.copy()
