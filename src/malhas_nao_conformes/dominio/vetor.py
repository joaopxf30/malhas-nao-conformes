import math


class Vetor:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __key(self):
        return self.x, self.y, self.z

    def __eq__(self, vetor: "Vetor"):
        return self.__key() == vetor.__key()

    def __hash__(self):
        return hash(self.__key())

    def __mul__(self, escalar: float) -> "Vetor":
        match escalar:
            case float():
                return self.__calcula_produto_escalar(escalar)

            case _:
                raise TypeError("Somente produto escalar está implementado")

    def __calcula_produto_escalar(self, escalar: float) -> "Vetor":
        x = escalar * self.x
        y = escalar * self.y
        z = escalar * self.z

        return Vetor(x, y, z)

    def calcula_norma_euclidiana(self) -> float:
        p_norma_2 = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

        return p_norma_2

    def calcula_produto_interno(self, vetor: "Vetor") -> float:
        produto_interno = (
            self.x * vetor.x +
            self.y * vetor.y +
            self.z * vetor.z
        )

        return produto_interno

    def calcula_produto_vetorial(self, vetor: "Vetor") -> "Vetor":
        x = self.y * vetor.z - self.z * vetor.y
        y = self.z * vetor.x - self.x * vetor.z
        z = self.x * vetor.y - self.y * vetor.x

        return Vetor(x, y, z)

    def normaliza(self) -> "Vetor":
        fator_normalizacao = 1/(self.calcula_norma_euclidiana())
        vetor_unitario = self * fator_normalizacao

        return vetor_unitario

    def obtem_vetor_oposto(self) -> "Vetor":
        x = -self.x
        y = -self.y
        z = -self.z

        return Vetor(x, y, z)

    def projeta_na_direcao(self, vetor: "Vetor") -> "Vetor":
        escalar = self.calcula_produto_interno(vetor)
        x = vetor.x * escalar
        y = vetor.y * escalar
        z = vetor.z * escalar

        return Vetor(x, y, z)

    def decompoe_em_base_ortonormal(self, vetor_normal_plano: "Vetor") -> "Vetor":
        vetor_perpendicular = self.projeta_na_direcao(vetor_normal_plano)
        vetor_plano = self - vetor_perpendicular






