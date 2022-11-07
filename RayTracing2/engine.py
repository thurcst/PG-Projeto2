import numpy as np
import math

from cena import Cena
from tqdm import tqdm


class RenderEngine:
    def __init__(self, background_color, cena: Cena) -> None:
        self.background_color = background_color
        self.cena = cena
        self.e = 10 ** (-5)  # Constant to prevent shadow acne

    def render(self):
        image = np.zeros((self.cena.altura, self.cena.largura, 3), dtype=np.uint8)

        # Criacao do sistema de coordenadas da camera {u,v,w}
        w = self.cena.w
        u = self.cena.u
        v = self.cena.v

        foco_camera = self.cena.foco

        # Lancamento dos raios
        q_00 = self.cena.q00

        for i in range(self.cena.altura):
            for j in range(self.cena.largura):
                q_ij = q_00 + self.cena.tamanho_pixel * (j * u - i * v)
                dir_ray = (q_ij - foco_camera) / np.linalg.norm(q_ij - foco_camera)
                pixel_color = self.cast(foco_camera, dir_ray)
                if max(pixel_color) > 1:
                    pixel_color = pixel_color / max(pixel_color)

                image[i][j] = pixel_color * np.array([255, 255, 255])
        return image

    def reflect(self, dir_light, surface_normal):
        # Returns the reflected light vector
        return 2 * np.inner(surface_normal, dir_light) * surface_normal - dir_light

    def tuple_comparator(self, object):
        return object[0]

    def shade(self, obj, intersection_point, dir_focus, surface_normal):
        """Função responsável por aplicar Phong Shading

        Args:
            obj (Esfera/Plano/Triangulo): Objeto a ser 'shadeado'
            intersection_point (np.array): ponto de interseção
            dir_focus (np.array): direção do foco
            surface_normal (np.array): vetor normal da superficie

        Returns:
            np.array: cor de um ponto específico após Phong shading
        """
        obj_color = obj.cor
        obj_ka = obj.k_a
        obj_kd = obj.k_d
        obj_ks = obj.k_s
        obj_exp = obj.exp

        # Calculates the ambient color influence
        point_color = obj_ka * obj_color * self.cena.ambient_light

        for light in self.cena.lights:
            point_to_light_vec = light.position - intersection_point
            light_dir = (point_to_light_vec) / np.linalg.norm(point_to_light_vec)

            reflected = self.reflect(light_dir, surface_normal)
            intersection_point_corrected = intersection_point + self.e * light_dir
            intersected_objs = self.trace(intersection_point_corrected, light_dir)

            closest_t = math.inf

            if intersected_objs:
                for t_obj in intersected_objs:
                    if t_obj[0] < closest_t:
                        closest_t = t_obj[0]

            if (
                not intersected_objs
                or np.inner(light_dir, (light.position - intersection_point_corrected))
                < closest_t
            ):
                if np.inner(surface_normal, light_dir) > 0:
                    point_color = (
                        point_color
                        + obj_kd
                        * obj_color
                        * (np.inner(surface_normal, light_dir))
                        * light.intensity
                    )
                if np.inner(dir_focus, reflected) > 0:
                    point_color = (
                        point_color
                        + (obj_ks * ((np.inner(dir_focus, reflected)) ** obj_exp))
                        * light.intensity
                    )

        return point_color

    def cast(self, foco_camera, dir_ray):
        point_color = self.background_color
        intersected_objs = self.trace(foco_camera, dir_ray)

        if intersected_objs:
            closest_t = math.inf
            closest_obj = None

            for t_obj in intersected_objs:
                if t_obj[0] < closest_t:
                    closest_t = t_obj[0]
                    closest_obj = t_obj[1]
                    # cor_background = closest_obj.color

            intersection_point = foco_camera + dir_ray * closest_t
            point_color = self.shade(
                closest_obj,
                intersection_point,
                -dir_ray,
                closest_obj.get_normal(intersection_point),
            )
        return point_color

    def trace(self, foco_camera, dir_ray):
        s = []
        for obj in self.cena.objetos:
            t = obj.intersect(foco_camera, dir_ray)
            if t:
                s.append((t, obj))
        return s

