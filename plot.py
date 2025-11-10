from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

from src.malhas_nao_conformes.dominio.paralelepipedo import Paralelepipedo
from src.malhas_nao_conformes.dominio.poligono import Poligono
from src.malhas_nao_conformes.dominio.segmento import Segmento


def plota_cubos(cubos: list[Paralelepipedo], cor='cyan', alpha=0.3, borda='k'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for cubo in cubos:
        for face in cubo.faces:
            xs = [p.x for p in face.vertices]
            ys = [p.y for p in face.vertices]
            zs = [p.z for p in face.vertices]
            verts = [list(zip(xs, ys, zs))]
            ax.add_collection3d(
                Poly3DCollection(verts, facecolors=cor, edgecolors=borda, alpha=alpha)
            )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_box_aspect([1, 1, 1])
    plt.show()

def visualiza_algoritmo(
    face_referencia: Poligono,
    face_incidente: Poligono,
    segmento: Segmento = None,
    paralelepipedos: list = None
):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # === Faces de referência e incidente ===
    coords_ref = [[p.x, p.y, p.z] for p in face_referencia.vertices]
    coords_inc = [[p.x, p.y, p.z] for p in face_incidente.vertices]

    ax.add_collection3d(
        Poly3DCollection([coords_ref], facecolors='magenta', alpha=0.5, edgecolors='k', linewidths=1)
    )
    ax.add_collection3d(
        Poly3DCollection([coords_inc], facecolors='blue', alpha=0.5, edgecolors='k', linewidths=1)
    )

    # === Segmento único (interseção) ===
    seg_coords = []
    if segmento:
        seg_coords = [
            [segmento.vertice_inicial.x, segmento.vertice_inicial.y, segmento.vertice_inicial.z],
            [segmento.vertice_final.x, segmento.vertice_final.y, segmento.vertice_final.z],
        ]
        xs, ys, zs = zip(*seg_coords)
        ax.plot(xs, ys, zs, color='red', linewidth=3, label='Segmento')

    if paralelepipedos:
        for cubo in paralelepipedos:
            for face in cubo.faces:
                # cada face é um Polígono com seus vértices
                vertices = face.vertices
                for i in range(len(vertices)):
                    v1 = vertices[i]
                    v2 = vertices[(i + 1) % len(vertices)]  # conecta em loop
                    ax.plot(
                        [v1.x, v2.x],
                        [v1.y, v2.y],
                        [v1.z, v2.z],
                        color='gray',
                        alpha=0.7,
                        linewidth=1
                    )

    # === Ajuste automático dos limites ===
    todos_pontos = coords_ref + coords_inc + (seg_coords if seg_coords else [])
    if paralelepipedos:
        for cubo in paralelepipedos:
            for face in cubo.faces:
                for v in face.vertices:
                    todos_pontos.append([v.x, v.y, v.z])

    xs_all, ys_all, zs_all = zip(*todos_pontos)
    ax.set_xlim(min(xs_all) - 0.5, max(xs_all) + 0.5)
    ax.set_ylim(min(ys_all) - 0.5, max(ys_all) + 0.5)
    ax.set_zlim(min(zs_all) - 0.5, max(zs_all) + 0.5)

    # === Estilo e rótulos ===
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('Visualização do Algoritmo Sutherland–Hodgman 3D')

    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend()
    plt.show()

