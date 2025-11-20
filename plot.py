import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from src.malhas_nao_conformes.dominio import Poliedro, Indice
from src.malhas_nao_conformes.regiao_contato import RegiaoContato


def plota_resultados_vizinhanca(
    elementos: list[Poliedro],
    indice: Indice,
    elemento_referente: Poliedro | None = None,
    regioes_contato: list[RegiaoContato] = None,
):
    """ Função orquestradora """
    # --- Plota o 3D ---
    plota_elemento_referente_e_incidentes(
        elementos=elementos,
        elemento_referente=elemento_referente,
        lista_contatos=regioes_contato,
    )

    if not regioes_contato:
        return

    # --- Agrupa regiões por face da referência ---
    vizinhos_por_face = defaultdict(list)
    for rc in regioes_contato:
        vizinhos_por_face[rc.face_referencia].append(rc)

    # --- Para cada face, gera um plot 2D independente ---
    for face_ref, contatos in vizinhos_por_face.items():
        plota_contatos_2d_por_face(
            face_referencia=face_ref,
            lista_contatos=contatos,
            indice=indice,
        )


def plota_elemento_referente_e_incidentes(
    elementos: list[Poliedro],
    elemento_referente: Poliedro | None = None,
    lista_contatos: list[RegiaoContato] = None,
):
    """ Cria sua própria figure/ax 3D """
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    # Malha completa
    for elemento in elementos:
        for face in elemento.faces:
            for aresta in face.arestas:
                ax.plot(
                    [aresta.vertice_inicial.x, aresta.vertice_final.x],
                    [aresta.vertice_inicial.y, aresta.vertice_final.y],
                    [aresta.vertice_inicial.z, aresta.vertice_final.z],
                    color="black", linewidth=0.5, alpha=0.25
                )

    # Elemento de referência
    if elemento_referente:
        for face in elemento_referente.faces:
            xs = [v.x for v in face.vertices]
            ys = [v.y for v in face.vertices]
            zs = [v.z for v in face.vertices]
            poly = Poly3DCollection(
                [list(zip(xs, ys, zs))],
                facecolor="salmon", edgecolor="black",
                linewidth=1.0, alpha=0.5, zorder=1000
            )
            ax.add_collection3d(poly)

    # Incidentes
    if lista_contatos:
        elementos_incidentes = {rc.elemento_incidente for rc in lista_contatos}
        for elemento in elementos_incidentes:
            for face in elemento.faces:
                xs = [v.x for v in face.vertices]
                ys = [v.y for v in face.vertices]
                zs = [v.z for v in face.vertices]
                poly = Poly3DCollection(
                    [list(zip(xs, ys, zs))],
                    facecolor="blue", edgecolor="black",
                    linewidth=1.0, alpha=0.05
                )
                ax.add_collection3d(poly)

    ax.view_init(elev=20, azim=50, roll=-1)
    ax.set_xlabel(r"$x$", fontsize=14)
    ax.set_ylabel(r"$y$", fontsize=14)
    ax.set_zlabel(r"$z$", fontsize=14)

    plt.tight_layout()
    plt.show()


def _projeta_para_2d(vertices, normal):
    normal = np.array([normal.x, normal.y, normal.z])
    normal /= np.linalg.norm(normal)

    aux = np.array([1, 0, 0]) if abs(normal[0]) < 0.9 else np.array([0, 1, 0])

    u = np.cross(normal, aux)
    u /= np.linalg.norm(u)
    v = np.cross(normal, u)

    xs, ys = [], []
    for p in vertices:
        p3 = np.array([p.x, p.y, p.z])
        xs.append(np.dot(p3, u))
        ys.append(np.dot(p3, v))

    return xs, ys


def plota_contatos_2d_por_face(face_referencia, lista_contatos, indice: Indice):
    """ Cada face cria sua própria figure/ax 2D """
    fig, ax = plt.subplots(figsize=(6, 6))

    # --- Face referência ---
    xs_ref, ys_ref = _projeta_para_2d(face_referencia.vertices, face_referencia.normal)
    ax.fill(xs_ref, ys_ref, color="lightgrey", alpha=0.4)
    ax.plot(xs_ref + [xs_ref[0]], ys_ref + [ys_ref[0]], color="black", linewidth=1.8)

    all_x, all_y = xs_ref.copy(), ys_ref.copy()

    for rc in lista_contatos:

        # Face incidente
        xs_fi, ys_fi = _projeta_para_2d(rc.face_incidente.vertices, face_referencia.normal)
        ax.fill(xs_fi, ys_fi, color="blue", alpha=0.15)
        ax.plot(xs_fi + [xs_fi[0]], ys_fi + [ys_fi[0]], color="blue", linewidth=1.2)

        # Região cortada
        xs_ri, ys_ri = _projeta_para_2d(rc.regiao_intersecao.vertices, face_referencia.normal)
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
            fr"$\mathsf{{C}}_{{{rc.indice_elemento_incidente}}}$",
            fontsize=13, ha="center", va="center",
            bbox=dict(facecolor="white", alpha=0.6, edgecolor='none')
        )

        area_corte = rc.regiao_intersecao.calcula_area()
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
