import numpy as np
from src import Orientacao
from src import Ponto
from src import Vetor


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

    def intersecta(self, segmento: "Segmento", normal_plano: Vetor) -> Ponto:

        def _determina_coeficientes(cooredenda: str):
            _coeficientes = [
                getattr(self.vertice_final, cooredenda) - getattr(self.vertice_inicial, cooredenda),
                getattr(segmento.vertice_final, cooredenda) - getattr(segmento.vertice_inicial, cooredenda)
            ]
            return _coeficientes

        def _determina_termo_independente(cooredenda: str):
            _termo_independente = (
                getattr(segmento.vertice_inicial, cooredenda) - getattr(self.vertice_inicial, cooredenda)
            )
            return _termo_independente

        x_normal = abs(normal_plano.x)
        y_normal = abs(normal_plano.y)
        z_normal = abs(normal_plano.z)

        if x_normal >= y_normal and x_normal >= z_normal:
            # Plano a ser projetado é o YZ
            coeficientes_equacao_1 = _determina_coeficientes("y")
            coeficientes_equacao_2 = _determina_coeficientes("z")
            termo_independente_equacao_1 = _determina_termo_independente("y")
            termo_independente_equacao_2 = _determina_termo_independente("z")

        elif y_normal >= x_normal and y_normal >= z_normal:
            # Plano a ser projetado é o ZX
            coeficientes_equacao_1 = _determina_coeficientes("z")
            coeficientes_equacao_2 = _determina_coeficientes("x")
            termo_independente_equacao_1 = _determina_termo_independente("z")
            termo_independente_equacao_2 = _determina_termo_independente("x")

        else:
            # Plano a ser projetado é o XY
            coeficientes_equacao_1 = _determina_coeficientes("x")
            coeficientes_equacao_2 = _determina_coeficientes("y")
            termo_independente_equacao_1 = _determina_termo_independente("x")
            termo_independente_equacao_2 = _determina_termo_independente("y")

        coeficientes = np.array([coeficientes_equacao_1, coeficientes_equacao_2])
        termos_independentes = np.array([termo_independente_equacao_1, termo_independente_equacao_2])

        escalar, _ = np.linalg.solve(coeficientes, termos_independentes)
        ponto = self.vertice_inicial + self.ordenamento * escalar

        return ponto
