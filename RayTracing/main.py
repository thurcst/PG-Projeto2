from engine import RenderEngine
from vetor import Vetor
from cena import Cena
from cor import Cor

from imagem import Imagem

from triangulo import Triangulo
from circulo import Circulo
from ponto import Ponto
from plano import Plano

import matplotlib.pyplot as plt
import numpy as np
import os
import json
import cv2


def main():

    path = "./objetos"

    cenas = []
    objetos = []

    for filename in os.listdir(path):
        if filename == "japao.json":
            f = os.path.join(path, filename)
            if os.path.isfile(f):
                file = open(f)
                text = json.load(file)
                cenas.append(text)
                file.close()

    cena = cenas[0]

    for element in cena["objects"]:
        form = list(element.keys())[1]
        props = element[form]

        print(form)

        if form == "sphere":
            obj = Circulo(
                np.array(props["center"]),
                props["radius"],
                Cor.from_rgb(element["color"]),
            )
            print(str(element.get("color", 0)))

        elif form == "plane":
            obj = Plano(
                np.array(props["sample"]),
                np.array(props["normal"]),
                Cor.from_rgb(element["color"]),
            )

        elif form == "triangle":
            obj = Triangulo(
                np.array(props["positions"]), Cor.from_rgb(element["color"])
            )

        objetos.append(obj)

    altura = cena.get("v_res", 0)
    largura = cena.get("h_res", 0)
    distancia = cena.get("dist", 0)
    square_side = cena.get("square_side", 0)

    up = np.array(cena.get("up", 0))
    eye = np.array(cena.get("eye", 0))
    look_at = np.array(cena.get("look_at", 0))

    w = (eye - look_at) / np.linalg.norm(eye - look_at)

    vec_prod = np.cross(up, w)

    u = (vec_prod) / (np.linalg.norm(vec_prod))
    v = np.cross(w, u)

    camera = eye - w * distancia

    camera_vetor = Vetor(camera[0], camera[1], camera[2])

    print(f"camera: ({camera[0]}, {camera[1]}, {camera[2]})")
    print(f"camera: {camera_vetor}")

    print(f"largura: {largura}, altura: {altura} ")

    print(objetos)

    cena = Cena(camera_vetor, objetos, largura, altura)

    engine = RenderEngine()
    imagem = engine.render(cena)

    with open("test.ppm", "w") as img_arq:
        imagem.escreve_ppm(img_arq)

    img = cv2.imread("./test.ppm")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite("imagem.jpg", img)
    print("Imagem salva.")


if __name__ == "__main__":
    main()

