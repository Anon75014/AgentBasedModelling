import numpy as np

class River:
    def __init__(self, water_content: float):
        self.default_water_content = water_content
        self.water_content = water_content

    def change_water_content(self, new_content: float):
        self.change_water_content = new_content

    def refresh_water_content(self):
        self.water_content = self.default_water_content

    def get_water(self, a: float) -> float:
        v = np.min([a, self.water_content])
        self.water_content = np.max([self.water_content - v, 0.0])
        return v
