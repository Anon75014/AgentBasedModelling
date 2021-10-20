import numpy as np
from enum import Enum, auto
from sim_map import Catchment

class Personality(Enum):
    """
    Personalities of the Farmers
    Maybe use Strategy design pattern for this?
    """
    Stocker = auto()
    Seller = auto()

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

