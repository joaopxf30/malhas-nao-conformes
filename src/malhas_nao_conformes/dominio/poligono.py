from abc import ABC, abstractmethod
from itertools import pairwise

from src import Indice
from src import Ponto
from src import Segmento


class Poligono(ABC):
    def __init__(self, vertices: list[Ponto], indice: Indice):
        self.vertices = vertices
        self.indice = indice
        self.arestas: list[Segmento] = self._determina_arestas()

    def _determina_arestas(self) -> list[Segmento]:
        ciclo_vertices = [*self.vertices, self.vertices[0]]
        arestas = []

        for vertice_anterior, vertice_posteior in pairwise(ciclo_vertices):
            aresta = Segmento(vertice_anterior, vertice_posteior)
            arestas.append(aresta)

        return arestas

    @abstractmethod
    def calcula_area(self) -> float:
        pass
