from cor import Cor

class Material:
    def __init__(self, cor=Cor.from_hex("#FFFFFF"), ambiente=0.05, difusa=1.0, especular=1.0):
        self.cor=cor
        self.ambiente=ambiente
        self.difusa=difusa
        self.especular=especular
    
    def cor_em(self, posicao):
        return self.cor
