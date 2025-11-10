from src.malhas_nao_conformes.dominio.paralelepipedo import Paralelepipedo
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.retangulo import Retangulo


def translada(
    paralelepipedo: Paralelepipedo,
    deslocamento_x: float,
    deslocamento_y: float,
    deslocamento_z: float
) -> Paralelepipedo:
    retangulos = []
    for faces in paralelepipedo.faces:
        vertices = []

        for vertice in faces.vertices:
            x = vertice.x + deslocamento_x
            y = vertice.y + deslocamento_y
            z = vertice.z + deslocamento_z
            vertices.append(Ponto(x, y, z))

        retangulos.append(Retangulo(vertices))

    return Paralelepipedo(retangulos)


