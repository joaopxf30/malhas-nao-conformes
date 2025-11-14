from abc import ABC, abstractmethod
from src.malhas_nao_conformes.dominio.poligono import Poligono
from src.malhas_nao_conformes.dominio.ponto import Ponto


class Poliedro(ABC):
    def __init__(self, faces: list[Poligono]):
        self.faces = faces
        self.vertices = self.__obtem_vertices()
        self.centro = self._obtem_centro_massa()

    @abstractmethod
    def _obtem_centro_massa(self) -> Ponto:
        pass

    def __obtem_vertices(self) -> list[Ponto]:
        vertices = []
        for face in self.faces:
            vertices.extend(face.vertices)

        return list(set(vertices))

