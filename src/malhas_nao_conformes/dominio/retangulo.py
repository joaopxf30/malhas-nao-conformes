from src.malhas_nao_conformes.dominio.indice import Indice
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.poligono import Poligono


class Retangulo(Poligono):
    def __init__(self, vertices: list[Ponto], indice: Indice = None):
        if len(vertices) != 4:
            raise ValueError("Retângulo só admite quatro vértices")

        super().__init__(vertices, indice)

    def __key(self):
        return self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, retangulo: "Retangulo"):
        return self.__key() == retangulo.__key()

    def _determina_centroide(self) -> Ponto:
        vertice_1 = self.vertices[0]
        vertice_2 = self.vertices[2]
        x = (vertice_1.x + vertice_2.x)/2
        y = (vertice_1.y + vertice_2.y)/2
        z = (vertice_1.z + vertice_2.z)/2

        return Ponto(x,y,z)

    def calcula_area(self) -> float:
        base = self.arestas[0].ordenamento.calcula_norma_euclidiana()
        altura = self.arestas[1].ordenamento.calcula_norma_euclidiana()

        return base * altura

    def checa_potencial_adjacencia(self, poligono: "Poligono") -> bool:

        def __verifica_intersecao_intervalo(
            min_intervalo_1: float,
            max_intervalo_1: float,
            min_intervalo_2: float,
            max_intervalo_2: float,
        ) -> bool:
            return (
                min_intervalo_1 <= min_intervalo_2 < max_intervalo_1
                or min_intervalo_1 < max_intervalo_2 <= max_intervalo_1
            )

        vertice_1 = self.vertices[0]
        vertice_2 = self.vertices[2]
        vertice_3 = poligono.vertices[0]
        vertice_4 = poligono.vertices[2]

        if self.indice.x:
            return (
                __verifica_intersecao_intervalo(
                    min(vertice_1.y, vertice_2.y),
                    max(vertice_1.y, vertice_2.y),
                    min(vertice_3.y, vertice_4.y),
                    max(vertice_3.y, vertice_4.y),
                )
                and __verifica_intersecao_intervalo(
                    min(vertice_1.z, vertice_2.z),
                    max(vertice_1.z, vertice_2.z),
                    min(vertice_3.z, vertice_4.z),
                    max(vertice_3.z, vertice_4.z),
                )
            )

        elif self.indice.y:
            return (
                __verifica_intersecao_intervalo(
                    min(vertice_1.x, vertice_2.x),
                    max(vertice_1.x, vertice_2.x),
                    min(vertice_3.x, vertice_4.x),
                    max(vertice_3.x, vertice_4.x),
                )
                and __verifica_intersecao_intervalo(
                    min(vertice_1.z, vertice_2.z),
                    max(vertice_1.z, vertice_2.z),
                    min(vertice_3.z, vertice_4.z),
                    max(vertice_3.z, vertice_4.z),
                )
            )

        else:
            return (
                __verifica_intersecao_intervalo(
                    min(vertice_1.x, vertice_2.x),
                    max(vertice_1.x, vertice_2.x),
                    min(vertice_3.x, vertice_4.x),
                    max(vertice_3.x, vertice_4.x),
                )
                and __verifica_intersecao_intervalo(
                    min(vertice_1.y, vertice_2.y),
                    max(vertice_1.y, vertice_2.y),
                    min(vertice_3.y, vertice_4.y),
                    max(vertice_3.y, vertice_4.y),
                )
            )

