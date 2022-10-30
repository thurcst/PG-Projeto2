from vetor import Vetor
from cor import Cor
from ponto import Ponto
from circulo import Circulo
from luz import Luz
from material import Material, PisoXadrez

LARGURA =320
ALTURA= 200
RENDERED_IMG="2balls.ppm"
CAMERA= Vetor(0,-0.35,-1)
OBJETOS=[Circulo(Ponto(0,10000.5,1),10000.0, 
PisoXadrez(cor1=Cor.from_hex("#420500"),
    cor2=Cor.from_hex("#e6b87d"),
    ambiente=0.2,
    reflexao=0.2)),
    Circulo(Ponto(0.75,-0.1,1),0.6, Material(Cor.from_hex("#0000FF")) ),
        Circulo(Ponto(-0.75,-0.1,2.25),0.6, Material(Cor.from_hex("#803980")) )]
LUZES= [Luz(Ponto(1.5,-0.5,-10.0), Cor.from_hex("#FFFFFF")),
    Luz(Ponto(-0.5,-10.5,0), Cor.from_hex("#E6E6E6"))]