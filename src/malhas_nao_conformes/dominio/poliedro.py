from abc import ABC, abstractmethod
from src.malhas_nao_conformes.dominio.poligono import Poligono
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.vetor import Vetor


class Poliedro(ABC):
    def __init__(self, faces: list[Poligono]):
        self.faces = faces
        self.vertices = self.__obtem_vertices()
        self.centro = self.__obtem_centro_massa()

    @abstractmethod
    def __obtem_centro_massa(self) -> Ponto:
        pass

    def __obtem_vertices(self) -> list[Ponto]:
        vertices = []
        for face in self.faces:
            vertices.append(face.vertices)

        return list(set(vertices))

