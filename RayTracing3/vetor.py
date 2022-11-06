import math

class Vetor:
    def __init__(self, x=0.0, y=0.0,z=0.0):
        self.x=x
        self.y=y
        self.z=z

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)
    
    def dot_product(self, outro):
        return self.x * outro.x + self.y * outro.y + self.z * outro.z
    
    def norma(self):
        return math.sqrt(self.dot_product(self))
    
    def normalizacao(self):
        return self/ self.norma()
    
    def __add__(self,outro):
        return Vetor(self.x + outro.x , self.y + outro.y, self.z + outro.z)
    
    def __sub__(self,outro):
        return Vetor(self.x - outro.x , self.y - outro.y, self.z - outro.z)
    
    def __mul__(self,outro):
        assert not isinstance(outro, Vetor)
        return Vetor(self.x * outro , self.y * outro, self.z * outro)

    def __rmul__(self,outro):
        return self.__mul__(outro)
    
    def __truediv__(self,outro):
        assert not isinstance(outro, Vetor)
        return Vetor(self.x / outro , self.y / outro, self.z / outro)