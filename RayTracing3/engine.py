from cena import Cena

import numpy as np
import math

from tqdm import tqdm

e = 10 ** (
    -5
)  # Constant to prevent shadow acne or that the secondary ray be generate inside the obj


class RenderEngine:
    def __init__(self, cena: Cena, background_color):
        self.cena = cena
        self.background_color = background_color

    def render(self,):
        image = np.zeros((self.cena.altura, self.cena.largura, 3), dtype=np.uint8)

        # Criacao do sistema de coordenadas da camera {u,v,w}
        w = self.cena.w
        u = self.cena.u
        v = self.cena.v

        # Lancamento dos raios
        q_00 = self.cena.q00

        for i in tqdm(range(self.cena.altura)):
            for j in range(self.cena.largura):
                q_ij = q_00 + self.cena.tamanho_pixel * (j * u - i * v)
                dir_ray = (q_ij - self.cena.foco) / np.linalg.norm(
                    q_ij - self.cena.foco
                )
                pixel_color = self.cast(self.cena.foco, dir_ray, self.cena.max_depth)
                if max(pixel_color) > 1:
                    pixel_color = pixel_color / max(pixel_color)

                image[i][j] = pixel_color * np.array([255, 255, 255])
        return image

    def reflect(self, dir_light, surface_normal):
        # Returns the reflected light vector
        return 2 * np.inner(surface_normal, dir_light) * surface_normal - dir_light

    def shade(self, obj, intersection_point, dir_focus, surface_normal):
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
            intersection_point_corrected = intersection_point + e * light_dir
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

    def refract(self, obj, observer_vec, normal_vec):
        refraction_index = obj.refraction_index
        cos_angle_normal_obs = np.inner(normal_vec, observer_vec)

        # Observador no meio interno
        if cos_angle_normal_obs < 0:
            normal_vec = -normal_vec
            refraction_index = 1 / refraction_index
            cos_angle_normal_obs = -cos_angle_normal_obs

        delta = 1 - (1 / (refraction_index ** 2)) * (1 - cos_angle_normal_obs ** 2)

        # Reflexão total: não há refração de luz
        if delta < 0:
            return None

        return (
            -(1 / refraction_index) * observer_vec
            - (math.sqrt(delta) - (1 / refraction_index) * cos_angle_normal_obs)
            * normal_vec
        )

    def cast(self, foco_camera, dir_ray, recursion_level):
        point_color = self.background_color
        intersected_objs = self.trace(foco_camera, dir_ray)

        if intersected_objs:
            closest_t = math.inf
            closest_obj = None

            for t_obj in intersected_objs:
                if t_obj[0] < closest_t:
                    closest_t = t_obj[0]
                    closest_obj = t_obj[1]

            intersection_point = foco_camera + dir_ray * closest_t
            observer_vec = -dir_ray
            normal = closest_obj.get_normal(intersection_point)
            point_color = self.shade(
                closest_obj, intersection_point, observer_vec, normal
            )

            if recursion_level > 0:
                reflected_cast = None

                # Calcula a contribuição da reflexão na cor do ponto
                if closest_obj.k_r > 0:
                    reflected_ray = self.reflect(observer_vec, normal)
                    intersection_point_corrected = (
                        intersection_point + e * reflected_ray
                    )

                    reflected_cast = self.cast(
                        intersection_point_corrected, reflected_ray, recursion_level - 1
                    )
                    reflected_color = closest_obj.k_r * reflected_cast
                    point_color = point_color + reflected_color

                # Calcula a contribuição da refração na cor do ponto
                if closest_obj.k_t > 0:
                    refracted_ray = self.refract(closest_obj, observer_vec, normal)
                    # Se não ocorrer reflexão total, continue o cálculo
                    if refracted_ray is not None:
                        intersection_point_corrected = (
                            intersection_point + e * refracted_ray
                        )
                        refracted_color = closest_obj.k_t * self.cast(
                            intersection_point_corrected,
                            refracted_ray,
                            recursion_level - 1,
                        )
                        point_color = point_color + refracted_color

                    # Realiza a reflexão total se k_r>0
                    elif reflected_cast is not None:
                        # Compensa a cor que deveria sera adicionada caso kr fosse 1
                        point_color += (1 - closest_obj.k_r) * reflected_cast

        return point_color

    def trace(self, foco_camera, dir_ray):
        s = []
        for obj in self.cena.objetos:
            t = obj.intersect(foco_camera, dir_ray)
            if t:
                s.append((t, obj))
        return s

