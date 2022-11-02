import numpy as np


class Plano:
    """Classe responsável por representar um Plano
    """

    def __init__(self, sample, normal, color=None) -> None:
        self.sample = np.array(sample)
        self.normal = np.array(normal)
        self.material = color

    def __str__(self):
        return f""" normal: {self.normal}
                    sample: {self.sample}
                """

