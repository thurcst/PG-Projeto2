from vetor import Vetor
from cena import Cena
from engine import RenderEngine
from cor import Cor
from imagem import Imagem
from ponto import Ponto
from circulo import Circulo
from luz import Luz
from material import Material
import importlib
import argparse
import os


def main():
    parser= argparse.ArgumentParser()
    parser.add_argument("cena",help="Caminho para o arquivo da cena(sem .py")
    args=parser.parse_args()
    mod = importlib.import_module(args.cena)

    cena=Cena(mod.CAMERA, mod.OBJETOS, mod.LUZES,mod.LARGURA,mod.ALTURA)
    engine= RenderEngine()
    imagem = engine.render(cena)
    os.chdir(os.path.dirname(os.path.abspath(mod.__file__)))
    with open(mod.RENDERED_IMG,"w") as img_arq:
        imagem.escreve_ppm(img_arq)

    
if __name__ == "__main__":
    main()
    