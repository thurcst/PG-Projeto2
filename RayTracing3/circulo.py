from math import sqrt
from vetor import Vetor

import numpy as np
import math


class Circulo:
    def __init__(
        self,
        centro,
        raioCircuferencia,
        material,
        ka,
        kd,
        ks,
        exp,
        kr,
        kt,
        refraction_index,
    ):
        self.centro = Vetor(centro[0], centro[1], centro[2])
        self.raioCircuferencia = raioCircuferencia
        self.material = material
        self.k_a = ka
        self.k_d = kd
        self.k_s = ks
        self.exp = exp
        self.kr = kr
        self.kt = kt
        self.refraction_index = refraction_index

    def intersect(self, ray_origin, ray_dir):
        l = self.centro - Vetor(ray_origin[0], ray_origin[1], ray_origin[2])
        _l = [self.centro.x, self.centro.y, self.centro.z] - ray_origin
        t_ca = np.inner(_l, ray_dir)
        # t_ca_v = Vetor(t_ca[0], t_ca[1], t_ca[2])

        inner = np.inner(_l, _l)

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
        center_to_point_vec = (point_on_object) - [center.x, center.y, center.z]
        norm = np.linalg.norm(center_to_point_vec)
        return center_to_point_vec / norm

    def __str__(self):
        return f"centro: {self.centro}, raio: {self.raioCircuferencia}, material: {self.material}"

