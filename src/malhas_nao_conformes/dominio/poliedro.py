from abc import ABC, abstractmethod
from src import Poligono
from src import Ponto


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

