from imagem import Imagem
from raioLuz import RaioLuz
from ponto import Ponto
from cor import Cor


class RenderEngine:

    MAX_PROFUNDIDADE = 5
    MIN_DISPLACE = 0.0001
    def render(self,cena):
        largura= cena.largura
        altura= cena.altura
        aspect_ratio= float(largura)/altura
        x0 = -1.0
        x1 = +1.0
        xpasso = (x1 - x0) / (largura-1)
        y0= -1.0/ aspect_ratio
        y1= +1.0/ aspect_ratio
        ypasso = (y1-y0)/(altura-1)

        camera= cena.camera
        pixels= Imagem(largura,altura)

        for i in range(altura):
            y= y0 + i *ypasso
            for j in range(largura):
                x = x0 + j * xpasso
                raioLuz = RaioLuz(camera, Ponto(x,y) - camera)
                pixels.set_pixel(j, i , self.tracadoRaio(raioLuz, cena))
                print("{:3.0f}%".format(float(i)/float(altura)*100),end="\r")
        return pixels

    def tracadoRaio(self, raioLuz, cena, profundidade=0):
        cor= Cor(0,0,0)
        dist_hit, obj_hit = self.achar_prox(raioLuz, cena)
        if obj_hit is None:
            return cor
        hit_pos = raioLuz.origem + raioLuz.direcao * dist_hit
        hit_normal = obj_hit.normal(hit_pos)
        cor += self.cor_em(obj_hit, hit_pos,hit_normal, cena)
        if profundidade < self.MAX_PROFUNDIDADE:
            novo_raioLuz_pos = hit_pos + hit_normal * self.MIN_DISPLACE
            novo_raioLuz_dir= raioLuz.direcao - 2 * raioLuz.direcao.dot_product(hit_normal)*hit_normal
            novo_raioLuz = RaioLuz(novo_raioLuz_pos, novo_raioLuz_dir)
            cor += self.tracadoRaio(novo_raioLuz,cena, profundidade+1)*obj_hit.material.reflexao
        return cor

    def achar_prox(self,raioLuz, cena):
        dist_min= None 
        obj_hit= None
        for obj in cena.objetos:
            dist = obj.intersecta(raioLuz)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return (dist_min, obj_hit)

    def cor_em(self, obj_hit, hit_pos, norma, cena):
        material= obj_hit.material
        obj_cor=material.cor_em(hit_pos)
        para_cam=cena.camera - hit_pos
        especular_k=50
        cor=material.ambiente * Cor.from_hex("#000000")
        for luz in cena.luzes:
            para_luz= RaioLuz(hit_pos,luz.posicao - hit_pos)
            cor +=(obj_cor * material.difusa * max(norma.dot_product(para_luz.direcao),0))
            metade_vetor = (para_luz.direcao + para_cam).normalizacao()
            cor +=(luz.cor * material.especular * max(norma.dot_product(metade_vetor),0) ** especular_k)
        return cor


    