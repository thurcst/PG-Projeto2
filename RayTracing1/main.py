from engine import RenderEngine
from cena import Cena

from triangulo import Triangulo
from circulo import Esfera
from plano import Plano

import matplotlib.pyplot as plt
import numpy as np
import json
import os


def read_objects(cena):

    objetos = []

    # iterar sobre os objetos da cena, criando cada um deles
    # usando as classes por nós definidas
    for element in cena["objects"]:
        keys = list(element.keys())

        if "sphere" in keys:
            form = "sphere"
        elif "plane" in keys:
            form = "plane"
        elif "triangle" in keys:
            form = "triangle"

        props = element[form]

        # Criamos baseado no nome dentro do objeto json

        if form == "sphere":
            obj = Esfera(np.array(props["center"]), props["radius"], element["color"],)

        elif form == "plane":
            obj = Plano(
                np.array(props["sample"]), np.array(props["normal"]), element["color"],
            )

        elif form == "triangle":
            obj = Triangulo(np.array(props), element["color"])

        objetos.append(obj)

    return objetos


def build_scene(objetos, cena):

    # Constantes tiradas a partir do JSON

    altura = cena.get("v_res", 0)
    largura = cena.get("h_res", 0)
    distancia = cena.get("dist", 0)
    tamanho_pixel = cena.get("square_side", 0)
    bc = cena.get("background_color", 0)
    up = np.array(cena.get("up", 0))
    foco = np.array(cena.get("eye", 0))
    distancia_focal = np.array(cena.get("look_at", 0))

    # Instância da classe Cor, pra facilitar integração com outros arquivos
    background_color = np.array(bc)

    # Constantes - aqui começa o processamento e a aplicação de funções de PG

    w = (foco - distancia_focal) / np.linalg.norm(foco - distancia_focal)
    vec_prod = np.cross(up, w)

    u = (vec_prod) / (np.linalg.norm(vec_prod))
    v = np.cross(w, u)

    q00 = (
        foco
        - distancia * w
        + tamanho_pixel * (((altura - 1) / 2) * v - ((largura - 1) / 2) * u)
    )

    # Montar a Cena
    cena = Cena(
        objetos,
        largura,
        altura,
        w,
        u,
        v,
        q00,
        vec_prod,
        tamanho_pixel,
        foco,
        distancia_focal,
    )

    return cena, background_color


def main():

    path = "./primeira_versao/objetos"

    cenas = []

    # Ainda é necessário adicionar um for superior pra iterar em todos os arquivos do path definido acima
    # assim teremos uma execução separada pra cada um deles

    # Leitura de cada arquivo dentro do Path
    for filename in os.listdir(path):
        if filename == "suzanne.json":
            f = os.path.join(path, filename)
            if os.path.isfile(f):
                file = open(f)
                text = json.load(file)
                cenas.append(text)
                file.close()

    # Pegamos apenas a primeira cena (motivos de desenvolvimento)
    cena = cenas[0]

    objetos = read_objects(cena)
    scene, background_color = build_scene(objetos, cena)

    engine = RenderEngine()
    imagem = engine.render(scene, background_color)

    plt.imshow(imagem)
    plt.show()


if __name__ == "__main__":
    main()

