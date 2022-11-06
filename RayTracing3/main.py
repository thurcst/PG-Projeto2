from engine import RenderEngine
from vetor import Vetor
from cena import Cena
from cor import Cor

from triangulo import Triangulo
from fonte_luz import light_source
from circulo import Circulo
from plano import Plano

import numpy as np
import os
import json
import cv2


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
        kt = element.get("kr", 0)
        refraction_index = element.get("index_of_refraction", 0)

        props = element[form]

        # Criamos baseado no nome dentro do objeto json

        if form == "sphere":
            obj = Circulo(
                np.array(props["center"]),
                props["radius"],
                Cor.from_rgb(element["color"]),
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
                Cor.from_rgb(element["color"]),
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
                Cor.from_rgb(element["color"]),
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

    lights = []

    for l in cena.get("lights", []):
        light = light_source(
            np.array(l.get("position", 0)), np.array(l.get("intensity", 0)) / 255
        )
        lights.append(light)

    # Instância da classe Cor, pra facilitar integração com outros arquivos
    background_color = Cor(bc[0], bc[1], bc[2])

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

    camera_vetor = Vetor(camera[0], camera[1], camera[2])

    # Montar a Cena
    cena = Cena(
        camera_vetor,
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
    )

    return cena, lights, background_color


def main():

    path = "./terceira_versao/objetos"

    cenas = []

    # Ainda é necessário adicionar um for superior pra iterar em todos os arquivos do path definido acima
    # assim teremos uma execução separada pra cada um deles

    # Leitura de cada arquivo dentro do Path
    for filename in os.listdir(path):
        if filename == "bolha2.json":
            f = os.path.join(path, filename)
            if os.path.isfile(f):
                file = open(f)
                text = json.load(file)
                cenas.append(text)
                file.close()

    # Pegamos apenas a primeira cena (motivos de desenvolvimento)
    cena = cenas[0]

    objetos = read_objects(cena)
    scene, lights, background_color = build_scene(objetos, cena)

    # ? Montar a engine e renderizar a cena
    #! Problema na etapa de renderizar
    engine = RenderEngine()
    # imagem = engine.render(cena, background_color)
    imagem = engine._render(scene, background_color, lights)

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

