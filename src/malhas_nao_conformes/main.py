from plot import plota_malha_indices, plota_malha_elemento_vizinhos
from src.malhas_nao_conformes.dominio import Indice
from src.malhas_nao_conformes.malha import Malha
from src.malhas_nao_conformes.utils import cria_malha


def processa_malha(malha: Malha, indice: Indice):
    elemento = malha.relacao_indice_elemento[indice]
    relacoes_vizinhanca = malha.obtem_regioes_contato_celula(elemento)
    plota_malha_elemento_vizinhos(malha.elementos, elemento, relacoes_vizinhanca)



if __name__ == '__main__':
    malha = cria_malha(
        comprimento_malha=10,
        largura_malha=8,
        altura_malha=6,
        numero_elementos_x=4,
        numero_elementos_y=4,
        numero_elementos_z=3,
        translacoes_z=True,
        translacoes_yz=True
    )
    processa_malha(malha, Indice(3,3,3))


