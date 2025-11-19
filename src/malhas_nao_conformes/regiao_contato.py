from src.malhas_nao_conformes.dominio import Poligono, Poliedro, Indice

FACE_REFERENCIA = 0
FACE_INCIDENTE = 1
REGIAO_CONTATO = 2
AREA_CONTATO = 3


class RegiaoContato:

    def __init__(
        self,
        indice_referencia: Indice,
        elemento_referencia:Poliedro,
        informacoes_contato: list[tuple[Poligono, Poliedro, Poligono, Indice, Poligono]],
    ):
        self.indice_referencia = indice_referencia
        self.elemento_referencia = elemento_referencia

        self.regiao_contato_por_face: dict[Indice, Poligono] = {}

        self.relacao_indice_elemento_incidente_elemento: dict[Indice, Poliedro] = {}
        self.relacao_indice_elemento_incidente_area_corte: dict[Indice, float] = {}

        self.__relaciona(informacoes_contato)

    def __str__(self):
        header = f"O elemento {self.indice_referencia} é vizinho aos elementos: \n"
        corpo = []
        for indice in self.relacao_indice_elemento_incidente.keys():


    def __relaciona(self, informacoes_contato: list[tuple[Poligono, Poliedro, Poligono, Indice, Poligono]]):
        for face_referencia, elemento_incidente, face_incidente, indice_elemento_incidente, regiao_corte in informacoes_contato:
            area_corte = regiao_corte.calcula_area()

            self.relacao_indice_elemento_incidente_elemento[indice_elemento_incidente] = elemento_incidente
            self.relacao_indice_elemento_incidente_area_corte[indice_elemento_incidente] = area_corte





