from input.translada import translada
from src.malhas_nao_conformes.dominio.hexaedro import Hexaedro
from src.malhas_nao_conformes.dominio.ponto import Ponto


cubo_1 = Hexaedro.inicializa_por_vertices(
    [
        Ponto(0, 0, 0),
        Ponto(1,0,0),
        Ponto(1,1,0),
        Ponto(0,1,0),
        Ponto(0,0,1),
        Ponto(1,0,1),
        Ponto(1,1,1),
        Ponto(0,1,1)
    ]
)

cubo_2 = translada(cubo_1, 1, -0.5, -0.5)
cubo_3 = translada(cubo_1, 1, -0.5, 0.5)
cubo_4 = translada(cubo_2, 0, 1, 0.25)
cubo_5 = translada(cubo_1, 0, 0, 1)
cubo_6 = translada(cubo_4, 0, 1, 0.25)


MALHA_1 = [cubo_1, cubo_2, cubo_3, cubo_4]