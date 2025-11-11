import numpy as np
from src.constants import Orientacao
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.vetor import Vetor


class Segmento:
    def __init__(self, vertice_inicial: Ponto, vertice_final: Ponto):
        self.vertice_inicial = vertice_inicial
        self.vertice_final = vertice_final
        self.ordenamento: Vetor = vertice_final - vertice_inicial

    def localiza_ponto(self, ponto: Ponto) -> Orientacao:
        vetor = ponto - self.vertice_inicial
        vetor_resultante = self.ordenamento.calcula_produto_vetorial(vetor)

        orientacao = vetor_resultante.z
        if orientacao > 0:
            return Orientacao.ESQUERDA

        elif orientacao < 0:
            return Orientacao.DIREITA

        else:
            return Orientacao.COLINEAR

    def intersecta(self, segmento: "Segmento") -> Ponto:
        coeficientes_equacao_1 = [
            self.vertice_final.x - self.vertice_inicial.x,
            segmento.vertice_inicial.x - segmento.vertice_final.x
        ]
        coeficientes_equacao_2 = [
            self.vertice_final.y - self.vertice_inicial.y,
            segmento.vertice_inicial.y - segmento.vertice_final.y
        ]
        coeficientes = np.array([coeficientes_equacao_1, coeficientes_equacao_2])

        termo_independente_equacao_1 = segmento.vertice_inicial.x - self.vertice_inicial.x
        termo_independente_equacao_2 = segmento.vertice_inicial.y - self.vertice_inicial.y
        termos_independentes = np.array([termo_independente_equacao_1, termo_independente_equacao_2])

        escalares = np.linalg.solve(coeficientes, termos_independentes)

        return escalares