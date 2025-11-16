import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Patch


def plota_malha_indices(elementos: list, relacao_elemento_indice: dict):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # ───────────────────────────────────────────────
    # 1) Plotar arestas de todos os elementos
    # ───────────────────────────────────────────────
    for elemento in elementos:
        for face in elemento.faces:
            for aresta in face.arestas:
                x = [aresta.vertice_inicial.x, aresta.vertice_final.x]
                y = [aresta.vertice_inicial.y, aresta.vertice_final.y]
                z = [aresta.vertice_inicial.z,  aresta.vertice_final.z]

                ax.plot(x, y, z, color="black", linewidth=1)

    # ───────────────────────────────────────────────
    # 2) Plotar índices no centro de cada elemento
    # ───────────────────────────────────────────────
    for elemento in elementos:
        indice = relacao_elemento_indice[elemento]
        cx, cy, cz = elemento.centro.x, elemento.centro.y, elemento.centro.z

        ax.text(cx, cy, cz,
                f"{indice}",
                color="red",
                ha="center", va="center")

    # ───────────────────────────────────────────────
    # 3) Ajustes visuais
    # ───────────────────────────────────────────────
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_box_aspect([1, 1, 1])  # mantém proporções corretas

    plt.show()


def plota_malha_arestas_destacando(elementos: list, elemento_destacado):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # ───────────────────────────────────────────────
    # 1) Plotar toda a malha como wireframe cinza
    # ───────────────────────────────────────────────
    for elemento in elementos:
        for face in elemento.faces:
            for aresta in face.arestas:
                x = [aresta.vertice_inicial.x, aresta.vertice_final.x]
                y = [aresta.vertice_inicial.y, aresta.vertice_final.y]
                z = [aresta.vertice_inicial.z, aresta.vertice_final.z]

                ax.plot(x, y, z, color=(0, 0, 0, 0.25), linewidth=0.8)

    # ───────────────────────────────────────────────
    # 2) Pintar o hexaedro destacado
    # ───────────────────────────────────────────────
    for face in elemento_destacado.faces:
        verts = [(v.x, v.y, v.z) for v in face.vertices]

        poly = Poly3DCollection(
            [verts],
            facecolors=(1, 0, 0, 0.35),   # vermelho suave (alpha 0.35)
            edgecolors="black",      # aresta em vermelho
            linewidths=1.2
        )
        ax.add_collection3d(poly)

    # ───────────────────────────────────────────────
    # 3) Ajuste visual
    # ───────────────────────────────────────────────
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_box_aspect([1, 1, 1])

    plt.show()

def plota_malha_com_destaques(malha, elemento_destacado=None, face_destacada=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # ==========================================================
    # 1) PLOTAR TODA A MALHA APENAS COM ARESTAS (wireframe)
    # ==========================================================
    for hexa in malha:
        for face in hexa.faces:
            # obter arestas como pares de vértices consecutivos
            verts = face.vertices
            for a, b in zip(verts, verts[1:] + verts[:1]):
                xs = [a.x, b.x]
                ys = [a.y, b.y]
                zs = [a.z, b.z]
                ax.plot(xs, ys, zs, linewidth=0.7, color="black")

    # ==========================================================
    # 2) PLOTAR UM ÚNICO HEXAEDRO COLORIDO (transparente)
    # ==========================================================
    if elemento_destacado:
        faces = [
            [(v.x, v.y, v.z) for v in face.vertices]
            for face in elemento_destacado.faces
        ]
        coll = Poly3DCollection(
            faces,
            facecolors="cyan",
            edgecolor="black",
            alpha=0.25
        )
        ax.add_collection3d(coll)

    # ==========================================================
    # 3) PLOTAR UMA ÚNICA FACE DESTACADA (bem marcada)
    # ==========================================================
    if face_destacada:
        face_coords = [(v.x, v.y, v.z) for v in face_destacada.vertices]
        coll_face = Poly3DCollection(
            [face_coords],
            facecolors="red",
            edgecolor="black",
            linewidths=2,
            alpha=0.7
        )
        ax.add_collection3d(coll_face)

    # ==========================================================
    # Ajustes de visualização
    # ==========================================================
    ax.set_box_aspect([1, 1, 1])  # mantém o cubo quadrado
    plt.tight_layout()
    plt.show()


def plota_arestas_com_destaques(elementos, elemento_destacado=None, face_destacada_1=None, face_destacada_2=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # ==========================================================
    # 1) PLOTAR TODA A MALHA APENAS COM ARESTAS (wireframe)
    # ==========================================================
    for elemento in elementos:
        for face in elemento.faces:
            verts = face.vertices
            for a, b in zip(verts, verts[1:] + verts[:1]):
                xs = [a.x, b.x]
                ys = [a.y, b.y]
                zs = [a.z, b.z]
                ax.plot(xs, ys, zs, linewidth=0.7, color="black")

    # ==========================================================
    # 2) DESTACAR UM ELEMENTO (hexaedro) INTEIRO
    # ==========================================================
    if elemento_destacado:
        faces = [
            [(v.x, v.y, v.z) for v in face.vertices]
            for face in elemento_destacado.faces
        ]
        coll = Poly3DCollection(
            faces,
            facecolors="cyan",
            edgecolor="black",
            alpha=0.25
        )
        ax.add_collection3d(coll)

    # ==========================================================
    # 3) DESTACAR UMA FACE
    # ==========================================================
    if face_destacada_1:
        coords = [(v.x, v.y, v.z) for v in face_destacada_1.vertices]
        coll_face = Poly3DCollection(
            [coords],
            facecolors="blue",
            edgecolor="black",
            linewidths=2,
            alpha=0.7
        )
        ax.add_collection3d(coll_face)

    # ==========================================================
    # 4) DESTACAR UMA OUTRA FACE
    # ==========================================================
    if face_destacada_2:
        coords = [(v.x, v.y, v.z) for v in face_destacada_2.vertices]
        coll_face = Poly3DCollection(
            [coords],
            facecolors="red",
            edgecolor="black",
            linewidths=2,
            alpha=0.7
        )
        ax.add_collection3d(coll_face)

    # ==========================================================
    # Ajuste visual
    # ==========================================================
    ax.set_box_aspect([1, 1, 1])
    plt.tight_layout()
    plt.show()


def plota_malha_elemento_vizinhos(
    elementos: list,
    elemento_principal,
    relacao_vizinhanca: list[tuple]  # (vizinho, area_de_contato)
):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # ======================================================
    # 1) ARESTAS DA MALHA (wireframe)
    # ======================================================
    for elemento in elementos:
        for face in elemento.faces:
            vs = face.vertices
            for a, b in zip(vs, vs[1:] + vs[:1]):
                ax.plot(
                    [a.x, b.x],
                    [a.y, b.y],
                    [a.z, b.z],
                    color="black",
                    linewidth=0.6
                )

    # ======================================================
    # 2) ELEMENTO PRINCIPAL (pintado)
    # ======================================================
    faces_principal = [
        [(v.x, v.y, v.z) for v in face.vertices]
        for face in elemento_principal.faces
    ]
    coll_principal = Poly3DCollection(
        faces_principal,
        facecolors="yellow",
        edgecolor="black",
        linewidths=1.2,
        alpha=0.45
    )
    ax.add_collection3d(coll_principal)

    # ======================================================
    # 3) ELEMENTOS VIZINHOS (pintados com outra cor)
    # ======================================================
    legend_handles = [
        Patch(facecolor="yellow", edgecolor="black", label="Elemento Principal")
    ]

    for vizinho, regiao in relacao_vizinhanca:
        faces_viz = [
            [(v.x, v.y, v.z) for v in face.vertices]
            for face in vizinho.faces
        ]
        coll_viz = Poly3DCollection(
            faces_viz,
            facecolors="cyan",
            edgecolor="black",
            linewidths=1.0,
            alpha=0.35
        )
        ax.add_collection3d(coll_viz)

        # ---------------------------------------------
        # Colocar rótulo no centro do vizinho
        # ---------------------------------------------
        cx, cy, cz = vizinho.centro.x, vizinho.centro.y, vizinho.centro.z
        ax.text(cx, cy, cz, f"{regiao.calcula_area():.3g}", color="blue")

        legend_handles.append(
            Patch(facecolor="cyan", edgecolor="black", label=f"Vizinho (área={regiao.calcula_area():.3g})")
        )

    # ======================================================
    # 4) Ajustes de visual e legenda
    # ======================================================
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_box_aspect([1, 1, 1])

    plt.legend(handles=legend_handles, loc="upper left", bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.show()


