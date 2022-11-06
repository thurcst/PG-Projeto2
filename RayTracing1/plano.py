import numpy as np
import math


class Plano:
    """Classe responsável por representar um Plano
    """

    def __init__(self, sample, normal, color) -> None:
        self.sample = np.array(sample)
        self.normal = np.array(normal)
        self.cor = color

    def intersect(self, ray_origin, ray_dir):
        """Retorna o ponto onde o ponto é intersectado

        Args:
            ray_origin (list): ponto de origem
            ray_dir (list): vetor de direção

        Returns:
            t: ponto onde o raio é intercectado
        """
        t = math.inf
        den = np.inner(ray_dir, self.normal)

        e = 10 ** (-6)  # constante para evitar erros de calculo

        if abs(den) > e:
            t = np.inner((self.sample - ray_origin), self.normal) / den
            if t < 0:
                # Raio não intersecta o plano
                return
            else:
                return t
        else:
            # Inner product between ray_dir and normal_vector too low
            return

    def get_normal(self, point_on_object=None):
        """Retorna a normal normalizada

        Args:
            point_on_object (list, optional): ponto no objeto. Defaults to None.

        Returns:
            list: normal
        """
        norm = np.linalg.norm(self.normal)
        return self.normal / norm

    def __str__(self):
        return f""" normal: {self.normal}
                    sample: {self.sample}
                """

