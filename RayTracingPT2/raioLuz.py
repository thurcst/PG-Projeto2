class RaioLuz:

    def __init__(self, origem, direcao):
        self.origem = origem
        self.direcao = direcao.normalizacao()