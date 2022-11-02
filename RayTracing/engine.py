from imagem import Imagem
from raioLuz import RaioLuz
from ponto import Ponto
from cor import Cor


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
                pixels.set_pixel(j, i, self.tracadoRaio(raioLuz, cena, backgroung_color))
        return pixels

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

