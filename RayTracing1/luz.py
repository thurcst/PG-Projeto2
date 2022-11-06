from cor import Cor
class Luz:
    def __init__(self, posicao, cor=Cor.from_hex("#FFFFFF")):
        self.posicao= posicao
        self.cor=cor