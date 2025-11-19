from src.malhas_nao_conformes.constants import Orientacao
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.vetor import Vetor


class Segmento:
    def __init__(self, vertice_inicial: Ponto, vertice_final: Ponto):
        self.vertice_inicial = vertice_inicial
        self.vertice_final = vertice_final
        self.ordenamento: Vetor = vertice_final - vertice_inicial

    def localiza_ponto(self, ponto: Ponto, normal_plano: Vetor) -> Orientacao:
        vetor = ponto - self.vertice_inicial
        produto_vetorial = self.ordenamento.calcula_produto_vetorial(vetor)
        orientacao = normal_plano.calcula_produto_interno(produto_vetorial)

        if orientacao > 0:
            return Orientacao.ESQUERDA

        elif orientacao < 0:
            return Orientacao.DIREITA

        else:
            return Orientacao.COLINEAR

    def intersecta_plano(self, ponto_plano: Ponto, vetor_normal_plano: Vetor) -> Ponto:
        produto_interno_inicial = vetor_normal_plano.calcula_produto_interno(
            self.vertice_inicial - ponto_plano
        )
        produto_interno_final = vetor_normal_plano.calcula_produto_interno(
            self.vertice_final - ponto_plano
        )

        escalar = produto_interno_inicial / (produto_interno_inicial - produto_interno_final)
        ponto = self.vertice_inicial + self.ordenamento * escalar

        return ponto
