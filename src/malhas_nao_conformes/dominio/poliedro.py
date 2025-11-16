from abc import ABC, abstractmethod
from src.malhas_nao_conformes.dominio.poligono import Poligono
from src.malhas_nao_conformes.dominio.indice import Indice
from src.malhas_nao_conformes.dominio.ponto import Ponto


class Poliedro(ABC):
    def __init__(self, faces: list[Poligono]):
        self.faces = faces
        self.vertices = self.__obtem_vertices()
        self.centro = self._obtem_centro_massa()
        self.relacao_indice_face: dict[Indice, Poligono] = {}
        self.relacao_face_indice: dict[Poligono, Indice] = {}

        if not self.relacao_indice_face or not self.relacao_face_indice:
            self.__relaciona()

    @abstractmethod
    def _obtem_centro_massa(self) -> Ponto:
        pass

    def __obtem_vertices(self) -> list[Ponto]:
        vertices = []
        for face in self.faces:
            vertices.extend(face.vertices)

        return list(set(vertices))

    def __relaciona(self):
        for face in self.faces:
            self.relacao_indice_face[face.indice] = face
            self.relacao_face_indice[face] = face.indice


