from src.malhas_nao_conformes.dominio.poliedro import Poliedro
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.retangulo import Retangulo


class Hexaedro(Poliedro):
    def __init__(self, faces: list[Retangulo]):
        for face in faces:
            if not isinstance(face, Retangulo):
                raise TypeError("A face deve ser uma instância de Retangulo")

        if len(faces) != 6:
            raise ValueError("Paralelepipedo admite apenas 6 faces.")

        super().__init__(faces)

    def _obtem_centro_massa(self) -> Ponto:
        coordenadas_x = []
        coordenadas_y = []
        coordenadas_z = []

        for vertice in self.vertices:
            coordenadas_x.append(vertice.x)
            coordenadas_y.append(vertice.y)
            coordenadas_z.append(vertice.z)

        x = sum(coordenadas_x)/len(coordenadas_x)
        y = sum(coordenadas_y)/len(coordenadas_y)
        z = sum(coordenadas_z)/len(coordenadas_z)

        return Ponto(x,y,z)

    @staticmethod
    def inicializa_por_vertices(vertices: list[Ponto]) -> "Hexaedro":
        """Gera uma instância da classe Hexaedro a partir dos vértices
        fornecidos em ordem aleatória. O próprio método é responsável por
        determinar as faces e seguir a convenção anti-horária de ordenamento
        dos vértices na face. Além disso, verifica que cada face do elemento
        seja perpendicular a um dos vetores canônicos do sistema cartesiano.
        """
        def __ordena_vertices_face_minima(_vertices: list[Ponto]) -> list[Ponto]:
            """Garante o ordenemento dos vértices no sentido anti-horário das faces mínimas
            """
            vertices_reordenados = [_vertices[0], _vertices[1], _vertices[3], _vertices[2]]

            return vertices_reordenados

        def __ordena_vertices_face_maxima(_vertices: list[Ponto]) -> list[Ponto]:
            """Garante o ordenemento dos vértices no sentido anti-horário das faces máximas
            """
            vertices_reordenados = [_vertices[0], _vertices[2], _vertices[3], _vertices[1]]

            return vertices_reordenados

        if len(vertices) != 8:
            raise ValueError("Elemento hexaedro necessita de 8 vértices para construção.")

        vertice_ordenados = sorted(vertices, key=lambda v: (v.x, v.y, v.z))
        x_inicial = vertice_ordenados[0].x
        y_inicial = vertice_ordenados[0].y
        z_inicial = vertice_ordenados[0].z

        listas = [[] for _ in range(6)]
        vetices_x_min, vertices_x_max, vertices_y_min, vertices_y_max, vertices_z_min, vertices_z_max = listas

        for vertice in vertice_ordenados:
            if vertice.x == x_inicial:
                vetices_x_min.append(vertice)
            else:
                vertices_x_max.append(vertice)

            if vertice.y == y_inicial:
                vertices_y_min.append(vertice)
            else:
                vertices_y_max.append(vertice)

            if vertice.z == z_inicial:
                vertices_z_min.append(vertice)
            else:
                vertices_z_max.append(vertice)

        face_x_min = Retangulo(__ordena_vertices_face_minima(vetices_x_min))
        face_y_min = Retangulo(__ordena_vertices_face_minima(vertices_y_min))
        face_z_min = Retangulo(__ordena_vertices_face_minima(vertices_z_min))
        face_x_max = Retangulo(__ordena_vertices_face_maxima(vertices_x_max))
        face_y_max = Retangulo(__ordena_vertices_face_maxima(vertices_y_max))
        face_z_max = Retangulo(__ordena_vertices_face_maxima(vertices_z_max))

        faces = [face_x_min, face_y_min, face_z_min, face_x_max, face_y_max, face_z_max]

        return Hexaedro(faces)

