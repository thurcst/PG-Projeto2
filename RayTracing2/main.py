from engine import RenderEngine
from luz import light_source
from cena import Cena

from triangulo import Triangulo
from circulo import Esfera
from plano import Plano

import matplotlib.pyplot as plt
import numpy as np
import json
import os

from datetime import datetime


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

        ka = element.get("ka", 0)  # Coef. ambiental
        ks = element.get("ks", 0)  # Coef. especular
        kd = element.get("kd", 0)  # Coef. difuso
        exp = element.get("exp", 0)  # Expoente de Phong

        props = element[form]

        # Criamos baseado no nome dentro do objeto json

        if form == "sphere":
            obj = Esfera(
                np.array(props["center"]),
                props["radius"],
                element["color"],
                ka,
                kd,
                ks,
                exp,
            )

        elif form == "plane":
            obj = Plano(
                np.array(props["sample"]),
                np.array(props["normal"]),
                element["color"],
                ka,
                kd,
                ks,
                exp,
            )

        elif form == "triangle":
            obj = Triangulo(np.array(props), element["color"], ka, kd, ks, exp,)

        objetos.append(obj)

    return objetos


def build_scene(objetos, cena):
    """Recebe as props do JSON de cena e cria o objeto

    Args:
        objetos (list): lista de Objetos da cena
        cena (dict): dict com os elementos da cena

    Returns:
        Cena: objeto da classe Cena com todos os atributos setados
        background_color: a cor de fundo da cena
    """

    altura = cena.get("v_res", 0)
    largura = cena.get("h_res", 0)
    distancia = cena.get("dist", 0)
    tamanho_pixel = cena.get("square_side", 0)
    bc = cena.get("background_color", 0)
    up = np.array(cena.get("up", 0))
    foco = np.array(cena.get("eye", 0))
    distancia_focal = np.array(cena.get("look_at", 0))
    ambient_light = np.array(cena.get("ambient_light", 0)) / 255

    lights = []

    for l in cena.get("lights", []):
        light = light_source(
            np.array(l.get("position", 0)), np.array(l.get("intensity", 0)) / 255
        )
        lights.append(light)

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
        lights,
        ambient_light,
    )

    return cena, background_color


def main():

    path = "./segunda_versao/objetos"

    cenas = []

    # Ainda é necessário adicionar um for superior pra iterar em todos os arquivos do path definido acima
    # assim teremos uma execução separada pra cada um deles

    # Leitura de cada arquivo dentro do Path

    cena_a_carregar = "chiclete.json"
    print("Vamos carregar a cena: " + cena_a_carregar)

    for filename in os.listdir(path):

        if filename == cena_a_carregar:
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

    engine = RenderEngine(background_color, scene)
    imagem = engine.render()

    plt.imshow(imagem)
    plt.show()


if __name__ == "__main__":
    main()

