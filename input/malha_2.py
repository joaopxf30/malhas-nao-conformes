from input.translada import translada
from src import Hexaedro
from src import Ponto


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

cubo_2 = translada(cubo_1, -0.1, 1, -0.1)
cubo_3 = translada(cubo_1, 0,0, 1)
cubo_4 = translada(cubo_2, 0,0, 1)
cubo_5 = translada(cubo_1, 1, 0, 0.1)
cubo_6 = translada(cubo_1, 0.9, 1, 0)
cubo_7 = translada(cubo_5, 0, 0, 1)
cubo_8 = translada(cubo_6, 0, 0, 1)

MALHA_2 = [
    cubo_1,
    cubo_2,
    cubo_3,
    cubo_4,
    cubo_5,
    cubo_6,
    cubo_7,
    cubo_8
]