import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from src.malhas_nao_conformes.dominio import Ponto, Vetor, Segmento


def plota_malha_elemento_destacado(
    output: str,
    elementos,
    elemento_referencia=None,
    elemento_incidente=None,
    face_referencia=None,
    face_incidente=None
):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=20, azim=50, roll=-1)

    # ---------------------------------------------------------
    # 1) MALHA COMPLETA — apenas arestas (sem cor nas faces)
    # ---------------------------------------------------------
    for elem in elementos:
        for face in elem.faces:
            vs = face.vertices
            xs = [v.x for v in vs] + [vs[0].x]
            ys = [v.y for v in vs] + [vs[0].y]
            zs = [v.z for v in vs] + [vs[0].z]
            ax.plot(xs, ys, zs, color="black", linewidth=0.6, zorder=5)

    # ---------------------------------------------------------
    # 2) ELEMENTO DE REFERÊNCIA (cinza clarinho)
    # ---------------------------------------------------------
    if elemento_referencia is not None:
        for face in elemento_referencia.faces:
            verts = [(v.x, v.y, v.z) for v in face.vertices]
            poly = Poly3DCollection(
                [verts],
                facecolor="salmon",
                edgecolor="black",
                linewidth=1.0,
                alpha=0.25,
                zsort="average",
                zorder=10
            )
            ax.add_collection3d(poly)

    # ---------------------------------------------------------
    # 3) ELEMENTO INCIDENTE (azul clarinho)
    # ---------------------------------------------------------
    if elemento_incidente is not None:
        for face in elemento_incidente.faces:
            verts = [(v.x, v.y, v.z) for v in face.vertices]
            poly = Poly3DCollection(
                [verts],
                facecolor="#ADD8E6",  # lightblue
                edgecolor="black",
                linewidth=1.0,
                alpha=0.25,
                zsort="average",
                zorder=10
            )
            ax.add_collection3d(poly)

    # ---------------------------------------------------------
    # 4) FACE DE REFERÊNCIA — destaque forte
    # ---------------------------------------------------------
    if face_referencia is not None:
        verts = [(v.x, v.y, v.z) for v in face_referencia.vertices]
        poly = Poly3DCollection(
            [verts],
            facecolor="red",
            edgecolor="black",
            linewidth=2.2,
            alpha=0.65,
            zsort="max",
            zorder=100
        )
        ax.add_collection3d(poly)

    # ---------------------------------------------------------
    # 5) FACE INCIDENTE — destaque forte
    # ---------------------------------------------------------
    if face_incidente is not None:
        verts = [(v.x, v.y, v.z) for v in face_incidente.vertices]
        poly = Poly3DCollection(
            [verts],
            facecolor="blue",
            edgecolor="black",
            linewidth=2.2,
            alpha=0.65,
            zsort="max",
            zorder=100
        )
        ax.add_collection3d(poly)

    # ---------------------------------------------------------
    # 6) Ticks inteiros de 2 em 2
    # ---------------------------------------------------------
    xs = [v.x for e in elementos for f in e.faces for v in f.vertices]
    ys = [v.y for e in elementos for f in e.faces for v in f.vertices]
    zs = [v.z for e in elementos for f in e.faces for v in f.vertices]

    ax.set_xticks(np.arange(int(min(xs)), int(max(xs))+1, 2))
    ax.set_yticks(np.arange(int(min(ys)), int(max(ys))+1, 2))
    ax.set_zticks(np.arange(int(min(zs)), int(max(zs))+1, 2))

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_zlabel(r"$z$")

    plt.tight_layout()
    plt.savefig(
        f"{output}.pdf",
        dpi=300,
        format="pdf",
        bbox_inches="tight",
        pad_inches=0
    )
    plt.show()


def plota_recorte(
    output: str,

    face_incidente=None,
    face_referencia=None,

    vetor_referencia=None,             # Vetor
    lista_vetores=None,                # list[Vetor]

    segmento_incidente=None,
    segmento_referencia=None,

    lista_pontos=None
):
    fig, ax = plt.subplots()
    ax.set_aspect("equal", adjustable="box")

    # ============================================================
    # AUXILIARES PARA PROJEÇÃO YZ
    # ============================================================

    def proj(p):
        """Projeção (x,y,z) -> (y,z)."""
        return p.y, p.z

    def desenha_face(face, cor, alpha=0.3, label=None):
        ys = [v.y for v in face.vertices] + [face.vertices[0].y]
        zs = [v.z for v in face.vertices] + [face.vertices[0].z]
        ax.fill(ys, zs, facecolor=cor, edgecolor="black",
                linewidth=2.0, alpha=alpha, label=label)

    def desenha_segmento(seg, cor, lw=3.0):
        y0, z0 = proj(seg.vertice_inicial)
        y1, z1 = proj(seg.vertice_final)
        ax.plot([y0, y1], [z0, z1], color=cor, linewidth=lw)

    def desenha_ponto(p, cor="black", size=60):
        y, z = proj(p)
        ax.scatter([y], [z], color=cor, s=size, zorder=1000)

    def desenha_vetor(origem, vetor, cor):
        oy, oz = proj(origem)
        ax.arrow(
            oy, oz,
            vetor.y, vetor.z,
            width=0.02,
            head_width=0.12,
            head_length=0.18,
            length_includes_head=True,
            color=cor
        )

    # ============================================================
    # ORIGEM DOS VETORES
    # ============================================================

    # origem dos vetores da lista = vértice inicial do segmento referência
    if segmento_referencia is not None:
        origem_lista = segmento_referencia.vertice_inicial
    else:
        origem_lista = None

    # origem do vetor referência = ponto médio
    if segmento_referencia is not None:
        v0 = segmento_referencia.vertice_inicial
        v1 = segmento_referencia.vertice_final
        origem_meio = type(v0)(
            (v0.x + v1.x) / 2,
            (v0.y + v1.y) / 2,
            (v0.z + v1.z) / 2
        )
    else:
        origem_meio = None

    # ============================================================
    # DESENHO DAS FACES
    # ============================================================
    if face_referencia is not None:
        desenha_face(face_referencia, cor="red", alpha=0.05,
                     label=r"$F_{1,1,2}^{i+}$")

    if face_incidente is not None:
        desenha_face(face_incidente, cor="blue", alpha=0.05,
                     label=r"$A_{2,1,2}^{i-}$")

    # ============================================================
    # DESENHO DOS SEGMENTOS
    # ============================================================
    if segmento_referencia is not None:
        desenha_segmento(segmento_referencia, cor="red")

    if segmento_incidente is not None:
        desenha_segmento(segmento_incidente, cor="blue")

    # ============================================================
    # DESENHO DO VETOR REFERÊNCIA
    # ============================================================
    if vetor_referencia is not None and origem_meio is not None:
        try:
            vetor_referencia = vetor_referencia.normaliza()
        except:
            pass

        desenha_vetor(origem_meio, vetor_referencia, "red")

    # ============================================================
    # DESENHO DOS VETORES DA LISTA
    # ============================================================
    if lista_vetores is not None and origem_lista is not None:
        for v in lista_vetores:
            desenha_vetor(origem_lista, v, "blue")

    # ============================================================
    # DESENHO DOS PONTOS
    # ============================================================
    if lista_pontos is not None:
        for p in lista_pontos:
            desenha_ponto(p)

    # ============================================================
    # CONFIGURAÇÕES FINAIS
    # ============================================================
    ax.set_xlabel("y", fontsize=16)
    ax.set_ylabel("z", fontsize=16)

    # aumentar fonte dos números dos eixos
    for tick in ax.get_xticklabels():
        tick.set_fontsize(12)
    for tick in ax.get_yticklabels():
        tick.set_fontsize(12)

    # grid mais visível
    ax.grid(True, linestyle="--", linewidth=0.7, alpha=0.5)

    # legenda no canto inferior direito
    ax.legend(loc="upper left", fontsize=13)

    plt.tight_layout()
    plt.savefig(f"{output}.pdf", dpi=300, format="pdf",
                bbox_inches="tight", pad_inches=0)
    plt.show()
