from src.malhas_nao_conformes.dominio.vetor import Vetor


class Ponto:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __key(self):
        return self.x, self.y, self.z

    def __eq__(self, ponto: "Ponto"):
        if not isinstance(ponto, Ponto):
            return False

        return self.__key() == ponto.__key()

    def __hash__(self):
        return hash(self.__key())

    def __add__(self, vetor: Vetor) -> "Ponto":
        if not isinstance(vetor, Vetor):
            raise TypeError("Operando deve ser da classe Vetor")

        x = self.x + vetor.x
        y = self.y + vetor.y
        z = self.z + vetor.z

        return Ponto(x, y, z)

    def __sub__(self, ponto: "Ponto") -> Vetor:
        if not isinstance(ponto, Ponto):
            raise TypeError("Operando deve ser da classe Ponto")

        x = self.x - ponto.x
        y = self.y - ponto.y
        z = self.z - ponto.z

        return Vetor(x, y, z)

    def busca_ponto_medio(self, outro: "Ponto") -> "Ponto":
        if not isinstance(outro, Ponto):
            raise TypeError("Operando deve ser da classe Ponto")

        ponto = self + (outro - self) * 0.5

        return ponto
