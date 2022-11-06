from math import sqrt
import numpy as np
import math


class Esfera:
    def __init__(self, centro, raioCircuferencia, cor):
        self.centro = centro
        self.raioCircuferencia = raioCircuferencia
        self.cor = np.array(cor)

    def intersect(self, ray_origin, ray_dir):
        l = self.centro - ray_origin
        t_ca = np.inner(l, ray_dir)

        inner = np.inner(l, l)

        d_2 = (inner) - (t_ca) ** 2

        if d_2 > (self.raioCircuferencia) ** 2:
            # Raio nao intersecta a esfera
            return
        else:
            t_hc = math.sqrt(self.raioCircuferencia ** 2 - d_2)
            t0 = t_ca - t_hc
            t1 = t_ca + t_hc
            if t0 > t1:
                t0, t1 = t1, t0
            if t0 < 0:
                if t1 < 0:
                    # Off-sColor_reen intersection with sphere
                    return None
                else:
                    return t1

            return t0

    def get_normal(self, point_on_object):
        center = self.centro
        center_to_point_vec = (point_on_object) - center
        norm = np.linalg.norm(center_to_point_vec)
        return center_to_point_vec / norm

