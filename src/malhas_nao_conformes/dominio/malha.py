from src.malhas_nao_conformes.dominio.poliedro import Poliedro
from src.malhas_nao_conformes.dominio.poligono import Poligono
from src.sutherland_hodgman import SutherlandHodgman

TOLERANCIA = 1e-3


class Malha:
    def __init__(self, elementos: list[Poliedro]):
        self.elementos = elementos
        self.indexacao: dict[tuple[int, int, int], Poliedro] = self.__gera_indexacao(elementos)

    def __gera_indexacao(self, elementos: list[Poliedro]) -> dict[tuple[int, int, int], Poliedro]:
        indexacao_estruturada = {}
        elementos_ordenados = sorted(elementos, key=lambda e: (e.centro.x, e.centro.y, e.centro.z))
        coord_x_referencia = elementos[0].centro.x
        coord_y_referencia = elementos[0].centro.y
        coord_z_referencia = elementos[0].centro.z
        i, j, k = 1, 1, 1

        for elemento in elementos_ordenados:
            if elemento.centro.x != coord_x_referencia:
                coord_x_referencia = elemento.centro.x
                coord_y_referencia = elemento.centro.y
                coord_z_referencia = elemento.centro.z
                i += 1

            if elemento.centro.y != coord_y_referencia:
                j += 1
            else:
                j = 1

                if elemento.centro.z != coord_z_referencia:
                    k += 1
                else:
                    k = 1

            indexacao_estruturada[(i,j,k)] = elemento

        return indexacao_estruturada

    def obtem_elementos_adjacentes(self, elemento: Poliedro) -> list[Poliedro] | None:
        elementos_adjacentes = []
        for face_referencia in elemento.faces:
            elementos = self.obtem_elementos_ajdacentes_por_face(face_referencia)
            elementos_adjacentes.extend(elementos)

        return elementos_adjacentes

    def obtem_elementos_ajdacentes_por_face(
        self,
        face: Poligono
    ) -> list[Poliedro]:
        normal = face.normal
        centroide = face.centroide

        elementos_adjacentes = []
        for elemento in self.elementos:
            normal_oposta = normal.obtem_vetor_oposto()
            face_candidata = elemento.face_por_normal.get(normal_oposta)
            centroide_candidato = face_candidata.centroide
            vetor = centroide - centroide_candidato
            projecao = vetor.projeta_na_direcao(normal_oposta)

            if projecao.calcula_norma_euclidiana() < TOLERANCIA:
                # visualiza_algoritmo(face, face_candidata, paralelepipedos=self.elementos)
                if SutherlandHodgman().recorte_geometrico(face, face_candidata):
                    elementos_adjacentes.append(elemento)

        return elementos_adjacentes
