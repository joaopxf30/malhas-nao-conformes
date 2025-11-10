from input.translada import translada
from src.malhas_nao_conformes.dominio.paralelepipedo import Paralelepipedo
from src.malhas_nao_conformes.dominio.ponto import Ponto
from src.malhas_nao_conformes.dominio.retangulo import Retangulo


cubo_1 = Paralelepipedo(
    faces=[
        Retangulo([Ponto(0, 0, 0), Ponto(0, 0, 1), Ponto(1, 0, 1), Ponto(1, 0, 0)]),
        Retangulo([Ponto(1, 0, 0), Ponto(1, 0, 1), Ponto(1, 1, 1), Ponto(1, 1, 0)]),
        Retangulo([Ponto(1, 1, 0), Ponto(1, 1, 1), Ponto(0, 1, 1), Ponto(0, 1, 0)]),
        Retangulo([Ponto(0, 0, 0), Ponto(0, 1, 0), Ponto(0, 1, 1), Ponto(0, 0, 1)]),
        Retangulo([Ponto(0, 0, 0), Ponto(1, 0, 0), Ponto(1, 1, 0), Ponto(0, 1, 0)]),
        Retangulo([Ponto(1, 1, 1), Ponto(1, 0, 1), Ponto(0, 0, 1), Ponto(0, 1, 1)]),
    ]
)

cubo_2 = translada(cubo_1, 1, 0.5, 0)
cubo_3 = translada(cubo_1, 1, 1.5, 0)
cubo_4 = translada(cubo_1, 1, -0.5, 0)
cubo_5 = translada(cubo_1, 0, 0, 1)

MALHA_1 = [cubo_1, cubo_2, cubo_3, cubo_4, cubo_5]