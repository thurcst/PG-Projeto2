class Cena:
    def __init__(
        self,
        camera,
        objetos,
        largura,
        altura,
        w,
        u,
        v,
        q00,
        vec_prod,
        tamanho_pixel,
        foco,
        distancia_focal,
        ambient_light,
    ):
        self.camera = camera
        self.objetos = objetos
        self.largura = largura
        self.altura = altura
        self.w = w
        self.u = u
        self.v = v
        self.q00 = q00
        self.tamanho_pixel = tamanho_pixel
        self.foco = foco
        self.distancia_focal = distancia_focal
        self.ambient_light = ambient_light
        self.vec_prod = vec_prod

