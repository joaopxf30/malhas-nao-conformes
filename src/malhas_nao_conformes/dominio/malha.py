from plot import visualiza_algoritmo
from src.malhas_nao_conformes.dominio.poliedro import Poliedro
from src.malhas_nao_conformes.dominio.poligono import Poligono
from src.sutherland_hodgman import SutherlandHodgman

TOLERANCIA = 1e-3


class Malha:
    def __init__(self, elementos: list[Poliedro]):
        self.elementos = elementos

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
