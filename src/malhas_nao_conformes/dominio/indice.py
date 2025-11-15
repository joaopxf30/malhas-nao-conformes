class Indice:
    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, indice: "Indice"):
        x = self.x + indice.x
        y = self.y + indice.y
        z = self.z + indice.z

        return Indice(x, y, z)

    def __sub__(self, indice: "Indice"):
        x = self.x - indice.x
        y = self.y - indice.y
        z = self.z - indice.z

        return Indice(x, y, z)