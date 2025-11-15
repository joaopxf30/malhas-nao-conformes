from plot import plota_adjacencias
from src.malhas_nao_conformes.dominio.indice import Indice
from src.malhas_nao_conformes.dominio.poliedro import Poliedro
from src.malhas_nao_conformes.dominio.poligono import Poligono
from src.malhas_nao_conformes.sutherland_hodgman import SutherlandHodgman

TOLERANCIA = 1e-3


class Malha:
    def __init__(self, elementos: list[Poliedro]):
        self.elementos = elementos
        self.relacao_indice_elemento: dict[Indice, Poliedro] = {}
        self.relacao_elemento_indice: dict[Poliedro, Indice] = {}

        if not self.relacao_indice_elemento or not self.relacao_elemento_indice:
            self.__relaciona()

    def __relaciona(self):
        elementos_ordenados = sorted(self.elementos, key=lambda e: (e.centro.x, e.centro.y, e.centro.z))
        coord_x_referencia = elementos_ordenados[0].centro.x
        coord_y_referencia = elementos_ordenados[0].centro.y
        coord_z_referencia = elementos_ordenados[0].centro.z
        i, j, k = 1, 1, 1

        for elemento in elementos_ordenados:
            plota_adjacencias(self.elementos, elemento, [])

            if elemento.centro.x != coord_x_referencia:
                coord_x_referencia = elemento.centro.x
                coord_y_referencia = elemento.centro.y
                coord_z_referencia = elemento.centro.z
                i += 1
                j = 1
                k = 1

            if elemento.centro.y != coord_y_referencia:
                coord_y_referencia = elemento.centro.y
                coord_z_referencia = elemento.centro.z
                j += 1
                k = 1

            if elemento.centro.z != coord_z_referencia:
                k += 1

            self.relacao_indice_elemento[Indice(i,j,k)] = elemento
            self.relacao_elemento_indice[elemento] = Indice(i,j,k)

    def obtem_relacao_vizinhanca(self, elemento: Poliedro) -> list[tuple[Poliedro, float]] | None:
        relacoes_vizinhanca = []
        for face in elemento.faces:
            visitados = set()
            if relacoes_vizinhanca_por_face := self.obtem_relacao_vizinhos_por_face(elemento, face, visitados):
                relacoes_vizinhanca.extend(relacoes_vizinhanca_por_face)

        return relacoes_vizinhanca

    def obtem_relacao_vizinhos_por_face(
        self,
        elemento: Poliedro,
        face: Poligono,
        visitados: set[Poliedro]
    ) -> list[Poliedro] | None:
        incremental = face.indice
        indice_vizinho = self.relacao_elemento_indice[elemento] + incremental
        elemento_vizinho = self.relacao_indice_elemento.get(indice_vizinho)
        visitados.add(elemento_vizinho)

        if elemento_vizinho is None:
            return elemento_vizinho

        for face in elemento.faces:
            visitados.add(face)

        visitados.add(indice_vizinho)

        for indice in indice_incremental.obtem_indices_perpendiculares():


        while True:
            if projecao.calcula_norma_euclidiana() < TOLERANCIA:
                # visualiza_algoritmo(face, face_candidata, paralelepipedos=self.elementos)
                if SutherlandHodgman().recorte_geometrico(face, face_candidata):
                    elementos_adjacentes.append(elemento)

        return elementos_adjacentes

    def _obtem_indices_perpendiculares(self, indice: Indice) -> list[Indice]:
        """Retorna as direções perpendiculares a tomada pelo índice
        """
        if indice.x:
            return [Indice(y=1), Indice(y=-1), Indice(z=1), Indice(z=-1)]

        elif indice.y:
            return [Indice(x=1), Indice(x=-1), Indice(z=1), Indice(z=-1)]

        else:
            return [Indice(x=1), Indice(x=-1), Indice(y=1), Indice(y=-1)]
