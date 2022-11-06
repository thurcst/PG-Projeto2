from math import sqrt
import numpy as np
import math


class Esfera:
    def __init__(self, centro, raioCircuferencia, cor, ka, kd, ks, exp):
        """Cria a instância da esfera

        Args:
            centro (np.array): coordenada do centro da esfera
            raioCircuferencia (float): raio da circunferência
            cor (np.array): cor (em RGB)
            ka (float): coeficiente ambiental
            kd (float): coeficiente difuso
            ks (float): coeficiente especular
            exp (float): expoente de Phong
        """
        self.centro = centro
        self.raioCircuferencia = raioCircuferencia
        self.cor = np.array(cor) / 255
        self.k_a = ka
        self.k_d = kd
        self.k_s = ks
        self.exp = exp

    def intersect(self, ray_origin, ray_dir):
        """identifica se o raio intersecta a esfera no ponto da sua direção

        Args:
            ray_origin (np.array): ponto de origem do raio
            ray_dir (np.array): vetor de direção do raio

        Returns:
            None || np.array : None ou ponto de interseção da esfera
        """
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
                    return None
                else:
                    return t1

            return t0

    def get_normal(self, point_on_object):
        """Retorna a normal já normalizada

        Args:
            point_on_object (np.array): Ponto no objeto

        Returns:
            np.array: a normal normalizada
        """
        center = self.centro
        center_to_point_vec = (point_on_object) - center
        norm = np.linalg.norm(center_to_point_vec)
        return center_to_point_vec / norm

