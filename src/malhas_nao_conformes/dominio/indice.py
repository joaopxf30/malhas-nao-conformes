class Indice:
    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    def __key(self):
        return self.x, self.y, self.z

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, indice: "Indice"):
        return self.__key() == indice.__key()

    def __add__(self, indice: "Indice") -> "Indice":
        x = self.x + indice.x
        y = self.y + indice.y
        z = self.z + indice.z

        return Indice(x, y, z)

    def __sub__(self, indice: "Indice") -> "Indice":
        x = self.x - indice.x
        y = self.y - indice.y
        z = self.z - indice.z

        return Indice(x, y, z)

    def __mul__(self, escalar: int) -> "Indice":
        x = self.x * escalar
        y = self.y * escalar
        z = self.z * escalar

        return Indice(x, y, z)

    def __str__(self) -> str:
        return f"{self.x}, {self.y}, {self.z}"

    def obtem_indices_perpendiculares(self) -> list["Indice"]:
        """Retorna as direções perpendiculares a tomada pelo índice
        """
        if self.x and not self.y and not self.z:
            return [Indice(y=1), Indice(z=1), Indice(y=-1), Indice(z=-1)]

        elif self.y and not self.x and not self.z:
            return [Indice(z=1), Indice(x=1), Indice(z=-1), Indice(x=-1)]

        elif self.z and not self.x and not self.y:
            return [Indice(x=1), Indice(y=1), Indice(x=-1), Indice(y=-1)]

        else:
            raise TypeError("A operação é válida somente para índice de faces")
