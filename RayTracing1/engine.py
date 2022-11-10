from cena import Cena

import numpy as np
import math


class RenderEngine:
    def render(self, cena: Cena, background_color):
        image = np.zeros((cena.altura, cena.largura, 3), dtype=np.uint8)

        # Criacao da base ortonormal {u,v,w}
        w = cena.w
        u = cena.u
        v = cena.v

        # Lancamento dos raios
        q_00 = cena.q00

        for i in range(cena.altura):
            print(f"{(i/cena.altura) * 100}% concluído")
            for j in range(cena.largura):
                q_ij = q_00 + cena.tamanho_pixel * (j * u - i * v)
                dir_ray = (q_ij - cena.foco) / np.linalg.norm(q_ij - cena.foco)
                image[i][j] = self.cast(cena, dir_ray, background_color)
        return image

    def trace(self, E, dir_ray, cena):
        s = []
        for obj in cena.objetos:
            t = obj.intersect(E, dir_ray)
            if t:
                s.append((t, obj))
        return s

    def cast(self, cena, dir_ray, background_color):
        E = cena.foco
        c = background_color
        S = self.trace(E, dir_ray, cena)

        if S:
            closest_t = math.inf
            closest_obj = None

            for t_obj in S:
                if t_obj[0] < closest_t:
                    closest_t = t_obj[0]
                    closest_obj = t_obj[1]
                    c = closest_obj.cor
        return c
