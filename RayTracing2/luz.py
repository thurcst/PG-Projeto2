class light_source:
    def __init__(self, position, intensity) -> None:
        self.position = position  # Localização (Si)
        self.intensity = intensity  # Cor (Ci)

    def __str__(self):
        txt = f"light = pos={self.position}  intensity={self.intensity}"
        return txt
