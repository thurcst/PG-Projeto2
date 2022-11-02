from vetor import Vetor


class RaioLuz:
    def __init__(self, origem: Vetor, direcao: Vetor):
        self.origem = origem
        self.direcao = direcao.normalizacao()
