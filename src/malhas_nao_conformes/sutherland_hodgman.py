from src.malhas_nao_conformes.constants import Orientacao, OrientacaoRecorte
from src.malhas_nao_conformes.dominio.poligono import Poligono
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.retangulo import Retangulo
from src.malhas_nao_conformes.dominio.segmento import Segmento
from src.malhas_nao_conformes.dominio.vetor import Vetor


class SutherlandHodgman:

    def obtem_regiao_contato(
        self,
        face_referencia: Poligono,
        face_incidente: Poligono
    ) -> Poligono | None:
        if face_incidente_plano := self.corta_face_incidente_no_plano_referencia(
            face_referencia,
            face_incidente
        ):
            regiao_contato = self.corta_face_incidente_na_face_referencia(
                face_referencia,
                face_incidente_plano
            )
            return regiao_contato

        else:
            return None

    def corta_face_incidente_no_plano_referencia(
        self,
        face_referencia: Poligono,
        face_incidente: Poligono,
    ) -> Poligono | None:
        vertice_referencia = face_referencia.vertices[0]
        vetor_plano_referencia = face_referencia.normal * -1.0

        vertices_recorte = []
        for aresta_incidente in face_incidente.arestas:
            vetor_inicial_incidente = aresta_incidente.vertice_inicial - vertice_referencia
            vetor_final_incidente =  aresta_incidente.vertice_final - vertice_referencia
            orientacao_inicial = self.__orientacao_recorte(vetor_inicial_incidente, vetor_plano_referencia)
            orientacao_final = self.__orientacao_recorte(vetor_final_incidente, vetor_plano_referencia)

            if orientacao_inicial != orientacao_final:
                vertice_intersecao = aresta_incidente.intersecta_plano(vertice_referencia, vetor_plano_referencia)
                vertices_recorte.append(vertice_intersecao)

            if orientacao_final == OrientacaoRecorte.DENTRO:
                vertices_recorte.append(aresta_incidente.vertice_final)

        if len(vertices_recorte) < 3:
            return None

        elif len(vertices_recorte) == 4:
            return Retangulo(vertices_recorte)

        else:
            raise NotImplementedError("Somente há suporte para geração de retângulos.")

    def corta_face_incidente_na_face_referencia(
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
                vertice_intersecao = aresta_referencia.intersecta_segmento(
                    aresta_incidente, normal_referencia
                )
                vertices.append(vertice_intersecao)

        elif orientacao_final == Orientacao.ESQUERDA:
            if orientacao_inicial == Orientacao.DIREITA:
                vertice_intersecao = aresta_referencia.intersecta_segmento(aresta_incidente, normal_referencia)
                vertices.append(vertice_intersecao)
            vertices.append(vertice_final)

        else:
            vertices.append(vertice_final)

        return vertices

    @staticmethod
    def __orientacao_recorte(
        vetor_incidente: Vetor,
        vetor_plano_referencia: Vetor
    ) -> OrientacaoRecorte:
        produto_interno = vetor_plano_referencia.calcula_produto_interno(vetor_incidente)
        if produto_interno >= 0:
            orientacao_corte = OrientacaoRecorte.DENTRO
        else:
            orientacao_corte = OrientacaoRecorte.FORA

        return orientacao_corte
