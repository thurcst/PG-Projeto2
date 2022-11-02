from engine import RenderEngine
from vetor import Vetor
from cena import Cena
from cor import Cor

from triangulo import Triangulo
from circulo import Circulo
from plano import Plano

import numpy as np
import os
import json
import cv2


def main():

    path = "./objetos"

    cenas = []
    objetos = []

    # Ainda é necessário adicionar um for superior pra iterar em todos os arquivos do path definido acima
    # assim teremos uma execução separada pra cada um deles

    # Leitura de cada arquivo dentro do Path
    for filename in os.listdir(path):
        if filename == "japao.json":
            f = os.path.join(path, filename)
            if os.path.isfile(f):
                file = open(f)
                text = json.load(file)
                cenas.append(text)
                file.close()

    # Pegamos apenas a primeira cena (motivos de desenvolvimento)
    cena = cenas[0]

    # iterar sobre os objetos da cena, criando cada um deles
    # usando as classes por nós definidas
    for element in cena["objects"]:
        form = list(element.keys())[1]
        props = element[form]

        # Criamos baseado no nome dentro do objeto json

        if form == "sphere":
            obj = Circulo(
                np.array(props["center"]),
                props["radius"],
                Cor.from_rgb(element["color"]),
            )

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

    # Constantes tiradas a partir do JSON
    altura = cena.get("v_res", 0)
    largura = cena.get("h_res", 0)
    distancia = cena.get("dist", 0)
    square_side = cena.get("square_side", 0)
    bc = cena.get("background_color", 0)
    up = np.array(cena.get("up", 0))
    eye = np.array(cena.get("eye", 0))
    look_at = np.array(cena.get("look_at", 0))

    # Instância da classe Cor, pra facilitar integração com outros arquivos
    background_color = Cor(bc[0], bc[1], bc[2])

    # Constantes - aqui começa o processamento e a aplicação de funções de PG

    w = (eye - look_at) / np.linalg.norm(eye - look_at)
    vec_prod = np.cross(up, w)

    u = (vec_prod) / (np.linalg.norm(vec_prod))
    v = np.cross(w, u)

    camera = eye - w * distancia

    camera_vetor = Vetor(camera[0], camera[1], camera[2])

    # Montar a Cena
    cena = Cena(camera_vetor, objetos, largura, altura)

    # ? Montar a engine e renderizar a cena
    #! Problema na etapa de renderizar
    engine = RenderEngine()
    imagem = engine.render(cena, background_color)

    # Salvar o arquivo como .ppm
    with open("test.ppm", "w") as img_arq:
        imagem.escreve_ppm(img_arq)

    # Ler o arquivo .ppm e salvar como jpg
    img = cv2.imread("./test.ppm")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite("imagem.jpg", img)
    print("Imagem salva.")


if __name__ == "__main__":
    main()

