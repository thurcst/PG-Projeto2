from imagem import Imagem
from raioLuz import RaioLuz
from ponto import Ponto
from cor import Cor
from cena import Cena

import numpy as np
import math


e = 10 ** (
    -5
)  # Constant to prevent shadow acne or that the secondary ray be generate inside the obj


class RenderEngine:
    def render(self, cena, backgroung_color):
        largura = cena.largura
        altura = cena.altura

        aspect_ratio = float(largura) / altura

        x0 = -1.0
        x1 = +1.0

        xpasso = (x1 - x0) / (largura - 1)

        y0 = -1.0 / aspect_ratio
        y1 = +1.0 / aspect_ratio

        ypasso = (y1 - y0) / (altura - 1)

        camera = cena.camera
        pixels = Imagem(largura, altura)

        for i in range(altura):
            y = y0 + i * ypasso
            for j in range(largura):
                x = x0 + j * xpasso
                raioLuz = RaioLuz(camera, Ponto(x, y) - camera)
                pixels.set_pixel(
                    j, i, self.tracadoRaio(raioLuz, cena, backgroung_color)
                )
        return pixels

    def _render(self, cena: Cena, background_color: Cor, lights):
        image = np.zeros((cena.altura, cena.largura, 3), dtype=np.uint8)

        background_color = [background_color.x, background_color.y, background_color.z]

        for i in range(cena.altura):
            for j in range(cena.largura):
                q_ij = cena.q00 + cena.tamanho_pixel * (j * cena.u - i * cena.v)
                direcao_ray = (q_ij - cena.foco) / np.linalg.norm(q_ij - cena.foco)
                cor_pixel = self.__cast__(
                    cena.foco, direcao_ray, background_color, lights, cena
                )

                if max(cor_pixel) > 1:
                    cor_pixel = [x / max(cor_pixel) for x in cor_pixel]

                image[i][j] = cor_pixel * np.array([255, 255, 255])
        return image

    def __trace__(self, foco_camera, dir_ray, objects) -> list:
        s = []
        for obj in objects:
            t = obj.intersect(foco_camera, dir_ray)
            if t:
                s.append((t, obj))
        return s

    def __cast__(
        self,
        foco_camera,
        dir_ray,
        background_color,
        lights,
        cena: Cena,
        recursion_level=0,
    ):
        point_color = background_color
        intersected_objs = self.__trace__(foco_camera, dir_ray, cena.objetos)

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
            point_color = self.__shade__(
                closest_obj, intersection_point, observer_vec, normal, lights, cena
            )

            if recursion_level > 0:
                reflected_cast = None

                # Calcula a contribuição da reflexão na cor do ponto
                if closest_obj.k_r > 0:
                    reflected_ray = self.__reflect__(observer_vec, normal)
                    intersection_point_corrected = (
                        intersection_point + e * reflected_ray
                    )

                    reflected_cast = self.__cast__(
                        intersection_point_corrected,
                        reflected_ray,
                        background_color,
                        lights,
                        cena,
                        recursion_level - 1,
                    )
                    reflected_color = closest_obj.k_r * reflected_cast
                    point_color = point_color + reflected_color

                # Calcula a contribuição da refração na cor do ponto
                if closest_obj.k_t > 0:
                    refracted_ray = self.__refract__(closest_obj, observer_vec, normal)
                    # Se não ocorrer reflexão total, continue o cálculo
                    if refracted_ray is not None:
                        intersection_point_corrected = (
                            intersection_point + e * refracted_ray
                        )
                        refracted_color = closest_obj.k_t * self.__cast__(
                            intersection_point_corrected,
                            refracted_ray,
                            background_color,
                            lights,
                            cena,
                            recursion_level - 1,
                        )
                        point_color = point_color + refracted_color

                    # Realiza a reflexão total se k_r>0
                    elif reflected_cast is not None:
                        # Compensa a cor que deveria sera adicionada caso kr fosse 1
                        point_color += (1 - closest_obj.k_r) * reflected_cast

        print(point_color)
        return point_color

    def __shade__(
        self, obj, intersection_point, dir_focus, surface_normal, lights, cena
    ):
        obj_color = obj.material
        obj_ka = obj.k_a
        obj_kd = obj.k_d
        obj_ks = obj.k_s
        obj_exp = obj.exp

        # Calculates the ambient color influence
        point_color = obj_ka * obj_color * cena.ambient_light

        for light in lights:
            point_to_light_vec = light.position - intersection_point
            light_dir = (point_to_light_vec) / np.linalg.norm(point_to_light_vec)

            reflected = self.__reflect__(light_dir, surface_normal)
            intersection_point_corrected = intersection_point + e * light_dir
            intersected_objs = self.__trace__(
                intersection_point_corrected, light_dir, cena.objetos
            )

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
                        [point_color.x, point_color.y, point_color.z]
                        + obj_kd
                        * obj_color
                        * (np.inner(surface_normal, light_dir))
                        * light.intensity
                    )
                if np.inner(dir_focus, reflected) > 0:
                    point_color = [point_color.x, point_color.y, point_color.z] + (
                        obj_ks * ((np.inner(dir_focus, reflected)) ** obj_exp)
                    ) * light.intensity

        return point_color

    def __reflect__(self, dir_light, surface_normal):
        # Returns the reflected light vector
        return 2 * np.inner(surface_normal, dir_light) * surface_normal - dir_light

    def tracadoRaio(self, raioLuz, cena, backgroung_color):
        cor = backgroung_color
        dist_hit, obj_hit = self.achar_prox(raioLuz, cena)
        if obj_hit is None:
            return cor
        hit_pos = raioLuz.origem + raioLuz.direcao * dist_hit
        cor += self.cor_em(obj_hit, hit_pos, cena)
        return cor

    def achar_prox(self, raioLuz, cena):
        dist_min = None
        obj_hit = None
        for obj in cena.objetos:
            dist = obj.intersecta(raioLuz)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return (dist_min, obj_hit)

    def cor_em(self, obj_hit, hit_pos, cena):
        return obj_hit.material

