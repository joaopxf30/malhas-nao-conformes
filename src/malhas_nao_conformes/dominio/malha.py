from plot import visualiza_algoritmo
from src.constants import Orientacao
from src.malhas_nao_conformes.dominio.paralelepipedo import Paralelepipedo
from src.malhas_nao_conformes.dominio.poligono import Poligono

TOLERANCIA = 1e-3


class Malha:
    def __init__(self, paralelepipedos: list[Paralelepipedo]):
        self.paralelepipedos = paralelepipedos

    def obtem_elementos_adjacentes(self, paralelepipedo_referencia: Paralelepipedo) -> list["Paralelepipedo"] | None:
        for face_referencia in paralelepipedo_referencia.faces:
            normal_referencia = face_referencia.normal
            centroide_referencia = face_referencia.centroide

            for paralelepipedo_incidente in self.paralelepipedos:
                normal_oposta_referencia = normal_referencia.obtem_vetor_oposto()
                face_incidente = paralelepipedo_incidente.face_por_normal.get(normal_oposta_referencia)
                centroide_incidente = face_incidente.centroide
                vetor = centroide_referencia - centroide_incidente
                vetor_projetado = vetor.projeta_na_direcao(normal_oposta_referencia)

                if vetor_projetado.calcula_norma_euclidiana() < TOLERANCIA:
                    visualiza_algoritmo(face_referencia, face_incidente, paralelepipedos=self.paralelepipedos)
                    self.recorte_geometrico_com_surtherland_hodgman(face_referencia, face_incidente)

    @staticmethod
    def recorte_geometrico_com_surtherland_hodgman(face_referencia: Poligono, face_incidente: Poligono):
        for aresta_referencia in face_referencia.arestas:
            # visualiza_algoritmo(face_referencia, face_incidente, aresta_referencia)

            for aresta_incidente in face_incidente.arestas:
                pontos = []

                vertice_incicial = aresta_incidente.vertice_inicial
                vertice_final = aresta_incidente.vertice_final
                orientacao_inicial = aresta_referencia.localiza_ponto(vertice_incicial)
                orientacao_final = aresta_referencia.localiza_ponto(vertice_final)

                if orientacao_final != Orientacao.DIREITA:
                    if orientacao_inicial == Orientacao.ESQUERDA:
                        vertice_intersecao = ...
                        pontos.append(vertice_intersecao)

                    pontos.append(vertice_final)
