from input.translada import translada
from src.malhas_nao_conformes.dominio.hexaedro import Hexaedro
from src.malhas_nao_conformes.dominio.ponto import Ponto


cubo_1 = Hexaedro.inicializa_por_vertices(
    [
        Ponto(0, 0, 0),
        Ponto(0, 0, 1),
        Ponto(1, 0, 1),
        Ponto(1, 0, 0),
        Ponto(1, 0, 0),
        Ponto(1, 0, 1),
        Ponto(1, 1, 1),
        Ponto(1, 1, 0)
    ]
)

cubo_2 = translada(cubo_1, 1, 0.5, 0)
cubo_3 = translada(cubo_1, 1, 1.5, 0)
cubo_4 = translada(cubo_1, 1, -0.5, 0)
cubo_5 = translada(cubo_1, 0, 0, 1)

MALHA_1 = [cubo_1, cubo_2, cubo_3, cubo_4, cubo_5]