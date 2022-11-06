class Imagem:
    def __init__(self, largura, altura):
        self.largura= largura
        self.altura= altura
        self.pixels= [[None for _ in range(largura)] for _ in range(altura)]

    def set_pixel(self, x, y, col):
        self.pixels[y][x] = col

    def escreve_ppm(self, img_arq):
        def to_byte(c):
            return round(max(min(c*255, 255),0))
        img_arq.write("P3 {} {}\n255\n".format(self.largura, self.altura))
        for linha in self.pixels:
            for cor in linha:
                img_arq.write("{} {} {} ".format(
                    to_byte(cor.x), to_byte(cor.y) ,to_byte(cor.z)
                ))

            img_arq.write("\n")