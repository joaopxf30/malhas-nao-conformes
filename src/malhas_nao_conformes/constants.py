from enum import Enum, auto


class Orientacao(Enum):
    COLINEAR = auto()
    DIREITA = auto()
    ESQUERDA = auto()


class OrientacaoRecorte(Enum):
    DENTRO = auto()
    FORA = auto()