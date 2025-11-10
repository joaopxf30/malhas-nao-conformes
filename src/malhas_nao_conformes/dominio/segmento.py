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