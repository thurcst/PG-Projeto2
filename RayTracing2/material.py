from cor import Cor

class Material:
    def __init__(self, cor=Cor.from_hex("#FFFFFF"), ambiente=0.05, difusa=1.0, especular=1.0, reflexao=0.5):
        self.cor=cor
        self.ambiente=ambiente
        self.difusa=difusa
        self.especular=especular
        self.reflexao = reflexao
    
    def cor_em(self, posicao):
        return self.cor

class PisoXadrez:
    def __init__(self, cor1=Cor.from_hex("#FFFFFF"), cor2=Cor.from_hex("#000000"), ambiente=0.05, difusa=1.0, especular=1.0, reflexao=0.5):
        self.cor1=cor1
        self.cor2=cor2
        self.ambiente=ambiente
        self.difusa=difusa
        self.especular=especular
        self.reflexao = reflexao
    
    def cor_em(self, posicao):
        if int((posicao.x + 5.0)*3.0)%2 == int(posicao.z*3.0)%2:
            return self.cor1
        else:
            return self.cor2

