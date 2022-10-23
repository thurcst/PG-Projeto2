from vetor import Vetor
from cena import Cena
from engine import RenderEngine
from cor import Cor
from imagem import Imagem
from ponto import Ponto
from circulo import Circulo

def main():
    LARGURA =320
    ALTURA= 200
    camera= Vetor(0,0,-1)
    objetos=[Circulo(Ponto(0,0,0), 0.5, Cor.from_hex("#FF0000"))]
    cena = Cena(camera, objetos, LARGURA, ALTURA)
    engine = RenderEngine()
    imagem = engine.render(cena)

    """im = Imagem(LARGURA, ALTURA)
    verm= Cor(x=1,y=0,z=0)
    verde= Cor(x=0,y=1,z=0)
    azul= Cor(x=0,y=0,z=1)

    im.set_pixel(0,0,verm)
    im.set_pixel(1,0,verde)
    im.set_pixel(2,0,azul)
    
    im.set_pixel(0,1,verm + verde)
    im.set_pixel(1,1,verm + azul+verde)
    im.set_pixel(2,1,verm * 0.001)
    """
    with open("test.ppm","w") as img_arq:
        imagem.escreve_ppm(img_arq)

    
if __name__ == "__main__":
    main()
    