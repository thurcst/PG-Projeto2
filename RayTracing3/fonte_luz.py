class light_source:
    def __init__(self, position, intensity) -> None:
        self.position = position
        self.intensity = intensity  # Cor da luz

    def __str__(self):
        txt = f"light = pos={self.position}  intensity={self.intensity}"
        return txt
