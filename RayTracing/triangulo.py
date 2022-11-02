import numpy as np


class Triangulo:
    def __init__(self, positions, color=None) -> None:
        self.positions = np.array(positions)
        self.material = color
