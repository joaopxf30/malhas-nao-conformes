from copy import deepcopy
from collections import deque

from plot import plota_malha_elemento_destacado
from src.malhas_nao_conformes.dominio import Ponto, Hexaedro
from src.malhas_nao_conformes.dominio.indice import Indice
from src.malhas_nao_conformes.dominio.poliedro import Poliedro
from src.malhas_nao_conformes.dominio.poligono import Poligono
from src.malhas_nao_conformes.sutherland_hodgman import SutherlandHodgman


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

    def obtem_regioes_contato_celula(self, elemento: Poliedro) -> list[tuple[Poliedro, Poligono, float]] | None:
        regioes = []
        for face in elemento.faces:
            incremento = face.indice
            indice_elemento_vizinho = self.relacao_elemento_indice[elemento] + incremento
            elemento_vizinho = self.relacao_indice_elemento.get(indice_elemento_vizinho)

            if elemento_vizinho is None:
                continue

            if regiao := self.obtem_regiao_contato_face(elemento_vizinho, face, elemento):
                regioes.append((face, elemento_vizinho, regiao))
                incrementos = incremento.obtem_indices_perpendiculares()
                regioes.extend(self.busca_celulas_em_largura(elemento_vizinho, incrementos, face))

        return regioes

    def obtem_regiao_contato_face(
        self,
        elemento_vizinho: Poliedro,
        face: Poligono,
        elemento = None
    ) -> Poligono | None:
        face_incidente = elemento_vizinho.relacao_indice_face.get(face.indice * -1)

        plota_malha_elemento_destacado("checagem_elementos", self.elementos, elemento, elemento_vizinho, face, face_incidente)

        if face.checa_potencial_adjacencia(face_incidente):
            regiao = SutherlandHodgman().obtem_regiao_contato(face, face_incidente)
            return regiao

        else:
            return None

    def busca_celulas_em_largura(
        self, elemento: Poliedro, incrementos: list[Indice], face: Poligono
    ) -> list[tuple[Poliedro, Poligono, float]]:
        regioes = []
        explorar = deque()
        visitados = set()
        explorar.append((elemento, incrementos))
        visitados.add(elemento)

        while explorar:
            elemento, incrementos = explorar.popleft()

            for contador, incremento in enumerate(incrementos):
                novos_incrementos = deepcopy(incrementos)
                indice_elemento_vizinho = self.relacao_elemento_indice[elemento] + incremento
                elemento_vizinho = self.relacao_indice_elemento.get(indice_elemento_vizinho)
                
                if elemento_vizinho is None or elemento_vizinho in visitados:
                    continue

                else:
                    visitados.add(elemento_vizinho)
                    if regiao := self.obtem_regiao_contato_face(elemento_vizinho, face):
                        regioes.append((face, elemento_vizinho, regiao))

                    else:
                        novos_incrementos.pop(contador)

                    explorar.append((elemento_vizinho, novos_incrementos))

        return regioes

    @staticmethod
    def descreve_malha(
        comprimento_malha: float,
        largura_malha: float,
        altura_malha: float,
        numero_elementos_x: int,
        numero_elementos_y: int,
        numero_elementos_z: int,
        translacoes_z_colunas_xy: list[float] = None,
        translacoes_y_colunas_x: list[float] = None,
    ) -> "Malha":
        """Descreve uma malha conforme composta de elementos hexaedros (cubos e paralelepípedos)
        e permite a aplicação de translações em z de cada coluna de elementos no plano xy, gerando
        não conformidade na malha. Além disso, permite translações em y de cada coluna de elementos
        em x.

        :param comprimento_malha: Tamanho na dimensão x na malha
        :param largura_malha: Tamanho na dimensão y na malha
        :param altura_malha: Tamanho na dimensão z na malha
        :param numero_elementos_x: Número de elementos na dimensão x na malha
        :param numero_elementos_y: Número de elementos na dimensão y na malha
        :param numero_elementos_z: Número de elementos na dimensão z na malha
        :param translacoes_z_colunas_xy: Lista de translações em z de cada coluna de elemento do plano xy
        :param translacoes_y_colunas_x: Vetor de translações em y de cada coluna de elementos em x
        :return: Malha de elementos hexaédricos
        """
        if (
            translacoes_z_colunas_xy
            and len(translacoes_z_colunas_xy) != numero_elementos_x * numero_elementos_y
        ):
            raise ValueError(
                f"É necessário informar {numero_elementos_x * numero_elementos_y} translações em z. "
                f"Uma para cada coluna de elementos em xy."
            )

        if translacoes_y_colunas_x and len(translacoes_y_colunas_x) != numero_elementos_x:
            raise ValueError(
                f"É necessário informar {numero_elementos_x} translações em y. "
                f"Uma para cada coluna de elementos em x."
            )

        comprimento_elemento = comprimento_malha/numero_elementos_x
        largura_elemento = largura_malha/numero_elementos_y
        altura_elemento = altura_malha/numero_elementos_z

        elementos = []
        x, contador_x, contador_xy = 0, 0, 0,
        for _ in range(numero_elementos_x):
            y = translacoes_y_colunas_x[contador_x]
            for _ in range(numero_elementos_y):
                z = translacoes_z_colunas_xy[contador_xy]
                for _ in range(numero_elementos_z):
                    vertice_1 = Ponto(x, y, z)
                    vertice_2 = Ponto(x, y + largura_elemento, z)
                    vertice_3 = Ponto(x, y, z + altura_elemento)
                    vertice_4 = Ponto(x, y + largura_elemento, z + altura_elemento)
                    vertice_5 = Ponto(vertice_1.x + comprimento_elemento, vertice_1.y, vertice_1.z)
                    vertice_6 = Ponto(vertice_2.x + comprimento_elemento, vertice_2.y, vertice_2.z)
                    vertice_7 = Ponto(vertice_1.x + comprimento_elemento, vertice_3.y, vertice_3.z)
                    vertice_8 = Ponto(vertice_1.x + comprimento_elemento, vertice_4.y, vertice_4.z)

                    hexaedro = Hexaedro.inicializa_por_vertices(
                        [vertice_1, vertice_2, vertice_3, vertice_4, vertice_5, vertice_6, vertice_7, vertice_8]
                    )
                    elementos.append(hexaedro)

                    z += altura_elemento
                contador_xy += 1
                y += largura_elemento
            contador_x += 1
            x += comprimento_elemento

        return Malha(elementos)


