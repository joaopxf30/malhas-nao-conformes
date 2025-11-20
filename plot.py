import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from src.malhas_nao_conformes.dominio import Indice
from src.malhas_nao_conformes.regiao_contato import RegiaoContato


def plota_resultados_vizinhanca(
    indice: Indice,
    regioes_contato: list[RegiaoContato] = None,
):
    if not regioes_contato:
        return

    vizinhos_por_face = defaultdict(list)
    for regiao_contato in regioes_contato:
        vizinhos_por_face[regiao_contato.face_referencia].append(regiao_contato)

    for face_referencia, regioes_contato in vizinhos_por_face.items():
        plota_contatos_2d_por_face(
            face_referencia=face_referencia,
            regioes_contato=regioes_contato,
            indice=indice,
        )

def _projeta_para_2d(vertices, normal):
    normal = np.array([normal.x, normal.y, normal.z])
    normal /= np.linalg.norm(normal)

    aux = np.array([1, 0, 0]) if abs(normal[0]) < 0.9 else np.array([0, 1, 0])

    u = np.cross(normal, aux)
    u /= np.linalg.norm(u)
    v = np.cross(normal, u)

    xs, ys = [], []
    for vertice in vertices:
        array_vertice = np.array([vertice.x, vertice.y, vertice.z])
        xs.append(np.dot(array_vertice, u))
        ys.append(np.dot(array_vertice, v))

    return xs, ys


def plota_contatos_2d_por_face(face_referencia, regioes_contato, indice: Indice):
    fig, ax = plt.subplots(figsize=(6, 6))

    xs_ref, ys_ref = _projeta_para_2d(face_referencia.vertices, face_referencia.normal)
    ax.fill(xs_ref, ys_ref, color="lightgrey", alpha=0.4)
    ax.plot(xs_ref + [xs_ref[0]], ys_ref + [ys_ref[0]], color="black", linewidth=1.8)

    all_x, all_y = xs_ref.copy(), ys_ref.copy()

    for regiao_contato in regioes_contato:

        xs_fi, ys_fi = _projeta_para_2d(regiao_contato.face_incidente.vertices, face_referencia.normal)
        ax.fill(xs_fi, ys_fi, color="blue", alpha=0.15)
        ax.plot(xs_fi + [xs_fi[0]], ys_fi + [ys_fi[0]], color="blue", linewidth=1.2)

        xs_ri, ys_ri = _projeta_para_2d(regiao_contato.regiao_intersecao.vertices, face_referencia.normal)
        ax.fill(xs_ri, ys_ri, color="salmon", alpha=0.6)
        ax.plot(xs_ri + [xs_ri[0]], ys_ri + [ys_ri[0]], color="darkred", linewidth=1.8)

        all_x += xs_ri
        all_y += ys_ri

        cx = np.mean(xs_ri)
        cy = np.mean(ys_ri)

        size_ref = max(max(all_x) - min(all_x), max(all_y) - min(all_y))
        dy = 0.05 * size_ref

        ax.text(
            cx, cy,
            fr"$\mathsf{{C}}_{{{regiao_contato.indice_elemento_incidente}}}$",
            fontsize=13, ha="center", va="center",
            bbox=dict(facecolor="white", alpha=0.6, edgecolor='none')
        )

        area_corte = regiao_contato.regiao_intersecao.calcula_area()
        ax.text(
            cx, cy - dy,
            f"{area_corte:.4f} u.a.",
            fontsize=10, ha="center", va="top",
            bbox=dict(facecolor="white", alpha=0.6, edgecolor='none')
        )

    xmin, xmax = min(all_x), max(all_x)
    ymin, ymax = min(all_y), max(all_y)
    dx = 0.15 * (xmax - xmin)
    dy = 0.15 * (ymax - ymin)

    ax.set_xlim(xmin - dx, xmax + dx)
    ax.set_ylim(ymin - dy, ymax + dy)

    ax.set_title(fr"$F^{{{face_referencia.indice}}}_{{{indice}(r)}}$", fontsize=14)
    ax.set_aspect("equal", "box")
    ax.grid(True)

    plt.tight_layout()
    plt.show()
