from src.malhas_nao_conformes.dominio import Poligono, Poliedro, Indice

FACE_REFERENCIA = 0
FACE_INCIDENTE = 1
REGIAO_CONTATO = 2
AREA_CONTATO = 3


class RegiaoContato:

    def __init__(
        self,
        face_referencia: Poligono,
        face_incidente: Poligono,
        regiao_intersecao: Poligono,
        elemento_incidente: Poliedro = None,
        indice_elemento_incidente: Indice = None,
    ):
        self.face_referencia = face_referencia
        self.face_incidente = face_incidente
        self.regiao_intersecao = regiao_intersecao
        self.elemento_incidente = elemento_incidente
        self.indice_elemento_incidente = indice_elemento_incidente

    def __str__(self):
        return f"Elemento ({self.indice_elemento_incidente}) com área de contato de {self.regiao_intersecao.calcula_area():.4f} u.a."

