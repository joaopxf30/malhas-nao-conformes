from plot import plota_malha_elemento_destacado, plota_tudo
from src.malhas_nao_conformes.dominio import Indice
from src.malhas_nao_conformes.malha import Malha
from src.malhas_nao_conformes.utils import cria_malha


def processa_malha(malha: Malha, indice: Indice):
    # plota_malha_elemento_destacado("malha_elemento_processar", malha.elementos, malha.relacao_indice_elemento.get(indice))
    regioes_contato = malha.obtem_regioes_contato_celula(indice)
    print(f"O elemento ({indice}) é vizinho das seguintes células:\n")
    for regiao_contato in regioes_contato:
        print(regiao_contato)

    elemento_referencia = malha.relacao_indice_elemento.get(indice)
    plota_tudo(malha.elementos, elemento_referencia, regioes_contato)

if __name__ == '__main__':
    malha = cria_malha(
        comprimento_malha=10,
        largura_malha=9,
        altura_malha=9,
        numero_elementos_x=2,
        numero_elementos_y=2,
        numero_elementos_z=2,
        translacoes_z=True,
        translacoes_yz=True
    )
    processa_malha(malha, Indice(1,2,2))


