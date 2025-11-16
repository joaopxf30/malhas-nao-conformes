from abc import ABC, abstractmethod
from itertools import pairwise

from src.malhas_nao_conformes.dominio.vetor import Vetor
from src.malhas_nao_conformes.dominio.indice import Indice
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.segmento import Segmento


class Poligono(ABC):
    def __init__(self, vertices: list[Ponto], indice: Indice = None):
        self.vertices = vertices
        self.indice = indice
        self.arestas: list[Segmento] = self.__determina_arestas()
        self.normal: Vetor = self.__determina_normal()

    @abstractmethod
    def calcula_area(self) -> float:
        pass

    @abstractmethod
    def checa_potencial_adjacencia(self, poligono: "Poligono") -> bool:
        pass

    def __determina_arestas(self) -> list[Segmento]:
        ciclo_vertices = [*self.vertices, self.vertices[0]]
        arestas = []

        for vertice_anterior, vertice_posteior in pairwise(ciclo_vertices):
            aresta = Segmento(vertice_anterior, vertice_posteior)
            arestas.append(aresta)

        return arestas

    def __determina_normal(self) -> Vetor:
        vetor_inicial = self.arestas[0].ordenamento
        vetor_final = self.arestas[1].ordenamento
        vetor_normal = vetor_inicial.calcula_produto_vetorial(vetor_final)
        vetor_normalizado = vetor_normal.normaliza()

        return vetor_normalizado
