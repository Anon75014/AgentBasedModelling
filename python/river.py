import numpy as np

class River:
    """This is the river class.
    """
    def __init__(self, water_content: float):
        """Initialisation

        :param water_content: Usual amount of water in the river.
        :type water_content: float
        """
        self.default_water_content = water_content
        self.water_content = water_content

    def change_water_content(self, new_content: float):
        """Change the content of the river

        :param new_content: Changes the current amount of water in the river.
        :type new_content: float
        """
        self.water_content = new_content

    def refresh_water_content(self):
        """
        Resets the `water_content` of the river
        """
        self.water_content = self.default_water_content

    def get_water(self, a: float) -> float:
        """
        Gets `a` amount of water from the river, which is deducted from the
        `water_content` of the river.

        :param a: Amount of water that is requested from the river
        :type a: float
        :return: `min(a, water_content)` so if the river is empty, it will return `0.0`.
        :rtype: float
        """
        v = np.min([a, self.water_content])
        self.water_content = np.max([self.water_content - v, 0.0])
        return v
