from src import Hexaedro
from src import Ponto
from src import Retangulo


def translada(
    paralelepipedo: Hexaedro,
    deslocamento_x: float,
    deslocamento_y: float,
    deslocamento_z: float
) -> Hexaedro:
    retangulos = []
    for face in paralelepipedo.faces:
        vertices = []

        for vertice in face.vertices:
            x = vertice.x + deslocamento_x
            y = vertice.y + deslocamento_y
            z = vertice.z + deslocamento_z
            vertices.append(Ponto(x, y, z))

        retangulos.append(Retangulo(vertices, face.indice))

    return Hexaedro(retangulos)


