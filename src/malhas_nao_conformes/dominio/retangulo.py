from src import Indice
from src import Ponto
from src import Poligono


class Retangulo(Poligono):
    def __init__(self, vertices: list[Ponto], indice: Indice):
        if len(vertices) != 4:
            raise ValueError("Retângulo só admite quatro vértices")

        super().__init__(vertices, indice)

    def __key(self):
        return self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, retangulo: "Retangulo"):
        return self.__key() == retangulo.__key()

    def _determina_centroide(self) -> Ponto:
        vertice_1 = self.vertices[0]
        vertice_2 = self.vertices[2]
        x = (vertice_1.x + vertice_2.x)/2
        y = (vertice_1.y + vertice_2.y)/2
        z = (vertice_1.z + vertice_2.z)/2

        return Ponto(x,y,z)

    def calcula_area(self) -> float:
        base = self.arestas[0].ordenamento.calcula_norma_euclidiana()
        altura = self.arestas[1].ordenamento.calcula_norma_euclidiana()

        return base * altura
