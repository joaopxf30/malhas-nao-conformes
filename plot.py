from collections import defaultdict

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from src.malhas_nao_conformes.dominio import Ponto, Vetor, Segmento, Poliedro
from src.malhas_nao_conformes.regiao_contato import RegiaoContato


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

    # ============================================================
    # AUXILIARES PARA PROJEÇÃO XY
    # ============================================================
    def proj(p):
        """Projeção (x,y,z) -> (x,y)."""
        return p.x, p.y

    def desenha_face(face, cor, alpha=0.3, label=None):
        xs = [v.x for v in face.vertices] + [face.vertices[0].x]
        ys = [v.y for v in face.vertices] + [face.vertices[0].y]
        ax.fill(xs, ys, facecolor=cor, edgecolor="black",
                linewidth=2.0, alpha=alpha, label=label)

    def desenha_segmento(seg, cor, lw=3.0):
        x0, y0 = proj(seg.vertice_inicial)
        x1, y1 = proj(seg.vertice_final)
        ax.plot([x0, x1], [y0, y1], color=cor, linewidth=lw)

    def desenha_ponto(p, cor="black", size=60):
        x, y = proj(p)
        ax.scatter([x], [y], color=cor, s=size, zorder=1000)

    def desenha_vetor(origem, vetor, cor):
        ox, oy = proj(origem)
        ax.arrow(
            ox, oy,
            vetor.x, vetor.y,
            width=0.02,
            head_width=0.12,
            head_length=0.18,
            length_includes_head=True,
            color=cor
        )    # ============================================================
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

def plota_tudo(
    elementos: list[Poliedro],
    elemento_destacado: Poliedro | None = None,
    lista_contatos: list[RegiaoContato] = None,
):

    grupos = defaultdict(list)
    if lista_contatos:
        for rc in lista_contatos:
            grupos[rc.face_referencia].append(rc)

    n = len(grupos)

    # FIGURA ÚNICA
    fig = plt.figure(figsize=(10, 6 + 3 * n))

    # ---- eixo 3D (linha 1) ----
    ax3d = fig.add_subplot(n + 1, 1, 1, projection="3d")

    plota_elementos_base(
        ax3d,
        elementos=elementos,
        elemento_destacado=elemento_destacado,
        lista_contatos=lista_contatos,
    )

    # ---- eixos 2D (resto das linhas) ----
    if n > 0:
        axes_2d = [
            fig.add_subplot(n + 1, 1, i + 2)
            for i in range(n)
        ]

        plota_contatos_2d_por_face(axes_2d, lista_contatos)

    plt.tight_layout()
    plt.show()

def plota_elementos_base(
    ax,
    elementos: list[Poliedro],
    elemento_destacado: Poliedro | None = None,
    lista_contatos: list[RegiaoContato] = None,
):

    # -----------------------------------
    # 1) Plotar arestas (malha)
    # -----------------------------------
    for elemento in elementos:
        for face in elemento.faces:
            for aresta in face.arestas:
                xs = [aresta.vertice_inicial.x, aresta.vertice_final.x]
                ys = [aresta.vertice_inicial.y, aresta.vertice_final.y]
                zs = [aresta.vertice_inicial.z, aresta.vertice_final.z]
                ax.plot(xs, ys, zs, color="black", linewidth=0.5, alpha=0.25)

    # Destacar elemento
    if elemento_destacado:
        for face in elemento_destacado.faces:
            xs = [v.x for v in face.vertices]
            ys = [v.y for v in face.vertices]
            zs = [v.z for v in face.vertices]
            verts = [list(zip(xs, ys, zs))]
            ax.add_collection3d(Poly3DCollection(
                verts, facecolor="yellow", edgecolor="black",
                linewidth=1.2, alpha=0.40
            ))

    # Destacar elementos de contato
    if lista_contatos:
        elementos_contato = {rc.elemento_incidente for rc in lista_contatos
                             if rc.elemento_incidente}

        for elemento in elementos_contato:
            for face in elemento.faces:
                xs = [v.x for v in face.vertices]
                ys = [v.y for v in face.vertices]
                zs = [v.z for v in face.vertices]
                verts = [list(zip(xs, ys, zs))]
                ax.add_collection3d(Poly3DCollection(
                    verts, facecolor="cyan", edgecolor="black",
                    linewidth=1, alpha=0.30
                ))

    ax.set_xlabel("X", fontsize=14)
    ax.set_ylabel("Y", fontsize=14)
    ax.set_zlabel("Z", fontsize=14)
    ax.set_title("Elementos e Elementos em Contato", fontsize=16)

def _projeta_para_2d(vertices, normal):
    """
    Projeta os vértices 3D para o plano da face usando base ortonormal (u, v).
    """
    normal = np.array([normal.x, normal.y, normal.z])
    normal = normal / np.linalg.norm(normal)

    # vetor auxiliar para gerar a base
    if abs(normal[0]) < 0.9:
        aux = np.array([1.0, 0.0, 0.0])
    else:
        aux = np.array([0.0, 1.0, 0.0])

    u = np.cross(normal, aux)
    u = u / np.linalg.norm(u)
    v = np.cross(normal, u)

    xs, ys = [], []
    for p in vertices:
        p3 = np.array([p.x, p.y, p.z])
        xs.append(np.dot(p3, u))
        ys.append(np.dot(p3, v))

    return xs, ys


def plota_contatos_2d_por_face(axes, lista_contatos):

    grupos = defaultdict(list)
    for rc in lista_contatos:
        grupos[rc.face_referencia].append(rc)

    for ax, (face_ref, contatos) in zip(axes, grupos.items()):

        xs, ys = _projeta_para_2d(face_ref.vertices, face_ref.normal)
        ax.fill(xs, ys, color="red", alpha=0.3)
        ax.plot(xs + [xs[0]], ys + [ys[0]], color="darkred", linewidth=2)

        for rc in contatos:
            xs_fi, ys_fi = _projeta_para_2d(rc.face_incidente.vertices, face_ref.normal)
            ax.fill(xs_fi, ys_fi, color="blue", alpha=0.2)
            ax.plot(xs_fi + [xs_fi[0]], ys_fi + [ys_fi[0]], color="blue", linewidth=1.5)

            xs_ri, ys_ri = _projeta_para_2d(rc.regiao_intersecao.vertices, face_ref.normal)
            ax.fill(xs_ri, ys_ri, color="green", alpha=0.5)
            ax.plot(xs_ri + [xs_ri[0]], ys_ri + [ys_ri[0]],
                    color="darkgreen", linewidth=2)

            cx = sum(xs_ri) / len(xs_ri)
            cy = sum(ys_ri) / len(ys_ri)
            ax.text(cx, cy,
                    f"{rc.indice_elemento_incidente}\nÁrea={rc.regiao_intersecao.calcula_area():.4f}",
                    fontsize=12,
                    ha="center",
                    bbox=dict(facecolor="white", alpha=0.7))

        ax.set_title(f"Face referência {face_ref.indice}", fontsize=14)
        ax.set_aspect("equal", "box")
        ax.grid(True)