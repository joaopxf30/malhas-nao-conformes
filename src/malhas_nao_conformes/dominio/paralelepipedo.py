from src.malhas_nao_conformes.dominio.poliedro import Poliedro
from src.malhas_nao_conformes.dominio.retangulo import Retangulo


class Paralelepipedo(Poliedro):
    def __init__(self, faces: list[Retangulo]):
        for face in faces:
            if not isinstance(face, Retangulo):
                raise TypeError("A face deve ser uma instância de Retangulo")

        if len(faces) != 6:
            raise ValueError("Paralelepipedo admite apenas 6 faces.")

        super().__init__(faces)