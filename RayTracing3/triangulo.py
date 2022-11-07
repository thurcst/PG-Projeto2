import numpy as np


class Triangulo:
    """Classe que representa um triângulo
    """

    def __init__(
        self, positions, color, ka, kd, ks, exp, kr, kt, refraction_index,
    ) -> None:
        self.positions = np.array(positions)
        self.cor = color
        self.k_a = ka
        self.k_d = kd
        self.k_s = ks
        self.exp = exp
        self.kr = kr
        self.kt = kt
        self.refraction_index = refraction_index


    def intersect(self, ray_origin, ray_dir):
        """Calcula se há, e a interseção de um raio no triangulo

        Args:
            ray_origin (list): ponto de origem
            ray_dir (list): vetor de direção

        Returns:
            t: ponto onde o raio é intercectado
        """

        v0v1 = self.positions[1] - self.positions[0]
        v0v2 = self.positions[2] - self.positions[0]

        e = 10 ** (-6)  # constante para evitar erros de calculo

        n = np.cross(v0v1, v0v2)

        NdotRayDirection = np.dot(n, ray_dir)

        if abs(NdotRayDirection) < e:
            return

        d = -np.dot(n, self.positions[0])
        t = -(np.dot(n, ray_origin) + d) / NdotRayDirection

        if t < 0:
            return

        p = ray_origin + t * ray_dir

        # Testaremos cada uma das pontas

        edge0 = self.positions[1] - self.positions[0]
        vp0 = p - self.positions[0]
        c = np.cross(edge0, vp0)

        if np.dot(n, c) < 0:
            return

        edge1 = self.positions[2] - self.positions[1]
        vp1 = p - self.positions[1]
        c = np.cross(edge1, vp1)

        if np.dot(n, c) < 0:
            return

        edge2 = self.positions[0] - self.positions[2]
        vp2 = p - self.positions[2]
        c = np.cross(edge2, vp2)

        if np.dot(n, c) < 0:
            return
        else:
            return t

    def get_normal(self, point_on_object=None):
        a = self.positions[1] - self.positions[0]
        b = self.positions[2] - self.positions[1]
        normal = np.cross(a, b)
        norm = np.linalg.norm(normal)
        return normal / norm

