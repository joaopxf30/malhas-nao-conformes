from src.malhas_nao_conformes.dominio.poligono import Poligono
from src.malhas_nao_conformes.dominio.vetor import Vetor


class Poliedro:
    def __init__(self, faces: list[Poligono]):
        self.faces = faces
        self.face_por_normal: dict[Vetor, Poligono] = self._determina_face_por_normal()

    def _determina_face_por_normal(self):
        face_por_normal = {}
        for face in self.faces:
            normal = face.normal
            face_por_normal[normal] = face

        return face_por_normal
