import numpy as np


class Triangulo:
    """Classe que representa um triângulo
    """
    def __init__(self, positions, color=None) -> None:
        self.positions = np.array(positions)
        self.material = color
