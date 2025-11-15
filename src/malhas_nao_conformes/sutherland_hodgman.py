from src.malhas_nao_conformes.constants import Orientacao
from src.malhas_nao_conformes.dominio.poligono import Poligono
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.retangulo import Retangulo
from src.malhas_nao_conformes.dominio.segmento import Segmento
from src.malhas_nao_conformes.dominio.vetor import Vetor


class SutherlandHodgman:

    def recorte_geometrico(
        self,
        face_referencia: Poligono,
        face_incidente: Poligono
    ) -> Poligono | None:
        normal_referencia = face_referencia.normal

        for aresta_referencia in face_referencia.arestas:
            vertices_incidentes = []

            for aresta_incidente in face_incidente.arestas:
                vertices_incidentes.extend(
                    self._determina_vertices_incidentes(
                        aresta_incidente,
                        aresta_referencia,
                        normal_referencia
                    )
                )

            if len(vertices_incidentes) != 4:
                return None

            face_incidente = Retangulo(vertices_incidentes)

        return face_incidente

    @staticmethod
    def _determina_vertices_incidentes(
        aresta_incidente: Segmento,
        aresta_referencia: Segmento,
        normal_referencia: Vetor,
    ) -> list[Ponto]:
        vertices = []

        vertice_inicial = aresta_incidente.vertice_inicial
        vertice_final = aresta_incidente.vertice_final
        orientacao_inicial = aresta_referencia.localiza_ponto(vertice_inicial, normal_referencia)
        orientacao_final = aresta_referencia.localiza_ponto(vertice_final, normal_referencia)

        if orientacao_final == Orientacao.DIREITA:
            if orientacao_inicial == Orientacao.ESQUERDA:
                vertice_intersecao = aresta_referencia.intersecta(
                    aresta_incidente, normal_referencia
                )
                vertices.append(vertice_intersecao)

        elif orientacao_final == Orientacao.ESQUERDA:
            if orientacao_inicial == Orientacao.DIREITA:
                vertice_intersecao = aresta_referencia.intersecta(aresta_incidente, normal_referencia)
                vertices.append(vertice_intersecao)
            vertices.append(vertice_final)

        else:
            vertices.append(vertice_final)

        return vertices
