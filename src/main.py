from input.malha_1 import MALHA_1
from plot import plota_cubos
from src.malhas_nao_conformes.dominio.malha import Malha


if __name__ == '__main__':
    malha = Malha(MALHA_1)
    for elemento in malha.elementos:
        elementos_adjacentes = malha.obtem_elementos_adjacentes(elemento)
        plota_cubos([*elementos_adjacentes, elemento])