import numpy as np


class Triangulo:
    """Classe que representa um triângulo
    """

    def __init__(
        self, positions, color, ka, kd, ks, exp, kr, kt, refraction_index,
    ) -> None:
        self.positions = np.array(positions)
        self.material = color
        self.k_a = ka
        self.k_d = kd
        self.k_s = ks
        self.exp = exp
        self.kr = kr
        self.kt = kt
        self.refraction_index = refraction_index
