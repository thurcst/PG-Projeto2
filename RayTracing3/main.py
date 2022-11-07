from engine import RenderEngine
from cena import Cena


from triangulo import Triangulo
from fonte_luz import light_source
from circulo import Circulo
from plano import Plano

import numpy as np
import os
import json
import matplotlib.pyplot as plt


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

        ka = element.get("ka", 0)
        ks = element.get("ks", 0)
        kd = element.get("kd", 0)
        exp = element.get("exp", 0)
        kr = element.get("kr", 0)
        kt = element.get("kt", 0)
        refraction_index = element.get("index_of_refraction", 0)

        props = element[form]

        # Criamos baseado no nome dentro do objeto json

        if form == "sphere":
            obj = Circulo(
                np.array(props["center"]),
                props["radius"],
                np.array(element["color"]) / 255,
                ka,
                kd,
                ks,
                exp,
                kr,
                kt,
                refraction_index,
            )

        elif form == "plane":
            obj = Plano(
                np.array(props["sample"]),
                np.array(props["normal"]),
                np.array(element["color"]) / 255,
                ka,
                kd,
                ks,
                exp,
                kr,
                kt,
                refraction_index,
            )

        elif form == "triangle":
            obj = Triangulo(
                np.array(props["positions"]),
                np.array(element["color"]) / 255,
                ka,
                kd,
                ks,
                exp,
                kr,
                kt,
                refraction_index,
            )

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
    ambient_light = np.array(cena.get("ambient_light", 0)) / 255

    max_depth = cena.get("max_depth", 0)

    lights = []

    for l in cena.get("lights", []):
        light = light_source(
            np.array(l.get("position", 0)), np.array(l.get("intensity", 0)) / 255
        )
        lights.append(light)

    background_color = np.array(bc)

    # Constantes - aqui começa o processamento e a aplicação de funções de PG

    w = (foco - distancia_focal) / np.linalg.norm(foco - distancia_focal)
    vec_prod = np.cross(up, w)

    u = (vec_prod) / (np.linalg.norm(vec_prod))
    v = np.cross(w, u)

    camera = foco - w * distancia
    Q00 = (
        camera
        + (0.5 * tamanho_pixel * (altura - 1) * v)
        - (0.5 * tamanho_pixel * (largura - 1) * u)
    )

    # Montar a Cena
    cena = Cena(
        objetos,
        largura,
        altura,
        w,
        u,
        v,
        Q00,
        vec_prod,
        tamanho_pixel,
        foco,
        distancia_focal,
        ambient_light,
        lights,
        max_depth,
    )

    return cena, background_color


def read_file(path, filename="bolha2.json"):
    cenas = []
    for filename in os.listdir(path):
        if filename == filename:
            f = os.path.join(path, filename)
            if os.path.isfile(f):
                file = open(f)
                text = json.load(file)
                cenas.append(text)
                file.close()
    cena = cenas[0]

    return cena


def main():
    path = "./terceira_versao/objetos"
    cena = read_file(path)
    objetos = read_objects(cena)
    scene, background_color = build_scene(objetos, cena)

    # Montar a engine e renderizar a cena

    engine = RenderEngine(scene, background_color)
    imagem = engine.render()
    return imagem


if __name__ == "__main__":

    imagem = main()
    plt.imshow(imagem)
    plt.show()

