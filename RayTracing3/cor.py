from vetor import Vetor
import numpy as np


class Cor(Vetor):
    @classmethod
    def from_rgb(cls, rgb):
        """Retorna a classe Cor a partir de uma entrada RGB

        Args:
            rgb (list): Lista com os valores RGB entre 0 e 255

        Returns:
            Cor: instância da classe Cor feita de acordo com valores RGB
        """

        x = float(rgb[0]) / 255
        y = float(rgb[1]) / 255
        z = float(rgb[2]) / 255

        print(f"r: {x}\ng: {y}\nb: {z}")
        return cls(x, y, z)

    @classmethod
    def from_hex(cls, hexcolor="#000000"):
        x = int(hexcolor[1:3], 16) / 255.0
        y = int(hexcolor[3:5], 16) / 255.0
        z = int(hexcolor[5:7], 16) / 255.0
        return cls(x, y, z)

    def __list__():
        return [super().x, super().y, super().z]
