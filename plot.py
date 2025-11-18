import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

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
