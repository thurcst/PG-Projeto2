from math import sqrt
from vetor import Vetor


class Circulo:
    def __init__(self, centro, raioCircuferencia, material):
        self.centro = Vetor(centro[0], centro[1], centro[2])
        self.raioCircuferencia = raioCircuferencia
        self.material = material

    def intersecta(self, raioLuz):
        circulo_para_raioLuz = raioLuz.origem - self.centro
        b = 2 * raioLuz.direcao.dot_product(circulo_para_raioLuz)
        c = (
            circulo_para_raioLuz.dot_product(circulo_para_raioLuz)
            - self.raioCircuferencia * self.raioCircuferencia
        )
        discriminante = b * b - 4 * c

        if discriminante >= 0:
            dist = (-b - sqrt(discriminante)) / 2
            if dist > 0:
                return dist
        return None

    def __str__(self):
        return f"centro: {self.centro}, raio: {self.raioCircuferencia}, material: {self.material}"

