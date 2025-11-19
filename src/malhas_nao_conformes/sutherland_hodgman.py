from plot import plota_recorte
from src.malhas_nao_conformes.constants import OrientacaoRecorte
from src.malhas_nao_conformes.dominio.poligono import Poligono
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.retangulo import Retangulo
from src.malhas_nao_conformes.dominio.vetor import Vetor


class SutherlandHodgman:

    def obtem_regiao_contato(
        self,
        face_referencia: Poligono,
        face_incidente: Poligono
    ) -> Poligono | None:
        vertice_referencia = face_referencia.vertices[0]
        vetor_plano_face_referencia = face_referencia.normal * -1.0
        # Recorta primeiro o polígono incidente com a face de referência
        if face_incidente := self.recorta_face(
            vertice_referencia,
            vetor_plano_face_referencia,
            face_incidente,
        ):
            # Recorta a face incidente projetada com a face de referência
            for aresta_referencia in face_referencia.arestas:
                vertice_referencia = aresta_referencia.vertice_inicial
                vetor_plano_referencia = aresta_referencia.ordenamento.calcula_produto_vetorial(vetor_plano_face_referencia)
                face_incidente = self.recorta_face(vertice_referencia, vetor_plano_referencia, face_incidente)

            return face_incidente

        else:
            return None

    def recorta_face(
        self,
        vertice_referencia: Ponto,
        normal_referencia: Vetor,
        face_incidente: Poligono,
    ) -> Poligono | None:

        vertices_recorte = []
        for aresta_incidente in face_incidente.arestas:
            vetor_inicial_incidente = aresta_incidente.vertice_inicial - vertice_referencia
            vetor_final_incidente =  aresta_incidente.vertice_final - vertice_referencia

            orientacao_inicial = self.__orientacao_recorte(vetor_inicial_incidente, normal_referencia)
            orientacao_final = self.__orientacao_recorte(vetor_final_incidente, normal_referencia)

            if orientacao_inicial != orientacao_final:
                vertice_intersecao = aresta_incidente.intersecta_plano(vertice_referencia, normal_referencia)
                vertices_recorte.append(vertice_intersecao)

            if orientacao_final == OrientacaoRecorte.DENTRO:
                vertices_recorte.append(aresta_incidente.vertice_final)

            # if face_referencia:
                # plota_recorte("corte_sutherland_hodgman.pdf",face_incidente, face_referencia, normal_referencia, [vetor_inicial_incidente, vetor_final_incidente], aresta_incidente, aresta_referencia, vertices_recorte)

        if len(vertices_recorte) < 3:
            return None

        elif len(vertices_recorte) == 4:
            return Retangulo(vertices_recorte, face_incidente.indice)

        else:
            raise NotImplementedError("Somente há suporte para geração de retângulos.")

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
