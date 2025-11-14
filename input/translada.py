from src.malhas_nao_conformes.dominio.hexaedro import Hexaedro
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.retangulo import Retangulo


def translada(
    paralelepipedo: Hexaedro,
    deslocamento_x: float,
    deslocamento_y: float,
    deslocamento_z: float
) -> Hexaedro:
    retangulos = []
    for faces in paralelepipedo.faces:
        vertices = []

        for vertice in faces.vertices:
            x = vertice.x + deslocamento_x
            y = vertice.y + deslocamento_y
            z = vertice.z + deslocamento_z
            vertices.append(Ponto(x, y, z))

        retangulos.append(Retangulo(vertices))

    return Hexaedro(retangulos)


