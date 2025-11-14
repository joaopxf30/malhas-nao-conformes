from abc import ABC, abstractmethod
from itertools import pairwise
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.segmento import Segmento
from src.malhas_nao_conformes.dominio.vetor import Vetor


class Poligono(ABC):
    def __init__(self, vertices: list[Ponto]):
        self.vertices = vertices
        self.arestas: list[Segmento] = self._determina_arestas()
        # self.normal: Vetor = self._determina_normal()
        # self.centroide: Ponto = self._determina_centroide()

    def _determina_arestas(self) -> list[Segmento]:
        ciclo_vertices = [*self.vertices, self.vertices[0]]
        arestas = []

        for vertice_anterior, vertice_posteior in pairwise(ciclo_vertices):
            aresta = Segmento(vertice_anterior, vertice_posteior)
            arestas.append(aresta)

        return arestas

    # def _determina_normal(self) -> Vetor:
    #     vetor_inicial = self.arestas[0].ordenamento
    #     vetor_final = self.arestas[1].ordenamento
    #     vetor_normal = vetor_inicial.calcula_produto_vetorial(vetor_final)
    #     vetor_normalizado = vetor_normal.normaliza()
    #
    #     return vetor_normalizado

    # @abstractmethod
    # def _determina_centroide(self) -> Ponto:
    #     pass

    @abstractmethod
    def calcula_area(self) -> float:
        pass
