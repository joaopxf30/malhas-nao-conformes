import random
from src.malhas_nao_conformes.malha import Malha


def cria_malha(
    comprimento_malha: float,
    largura_malha: float,
    altura_malha: float,
    numero_elementos_x: int,
    numero_elementos_y: int,
    numero_elementos_z: int,
    translacoes_z: bool = False,
    translacoes_yz: bool = False,
) -> Malha:
    if translacoes_z:
        translacoes_z_colunas_xy = [
            random.uniform(-0.5, 0.5) for _ in range(
                numero_elementos_x * numero_elementos_y
            )
        ]
    else:
        translacoes_z_colunas_xy = None

    if translacoes_yz:
        translacoes_y_colunas_x = [
            random.uniform(-0.5, 0.5) for _ in range(
                numero_elementos_x
            )
        ]
    else:
        translacoes_y_colunas_x = None

    return Malha.descreve_malha(
        comprimento_malha,
        largura_malha,
        altura_malha,
        numero_elementos_x,
        numero_elementos_y,
        numero_elementos_z,
        translacoes_z_colunas_xy,
        translacoes_y_colunas_x,
    )