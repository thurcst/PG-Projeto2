from vetor import Vetor
import numpy as np


class Cor(Vetor):
    @classmethod
    def from_rgb(cls, rgb):
        x = float(rgb[0])/255
        y = float(rgb[1])/255
        z = float(rgb[2])/255

        print(x,y,z)
        return cls(x, y, z)

    @classmethod
    def from_hex(cls, hexcolor="#000000"):
        x = int(hexcolor[1:3], 16) / 255.0
        y = int(hexcolor[3:5], 16) / 255.0
        z = int(hexcolor[5:7], 16) / 255.0
        return cls(x, y, z)

