#Prac_2
import networkx as nx
import random
#Simulació
NOMFITXER = "lastfm_asia_edges.csv"

import matplotlib.pyplot as plt
import numpy as np

def draw_graph(G: nx.Graph):
    pos = nx.spring_layout(G, seed=42, k=0.3)  # Mejor disposición
    
    plt.figure(figsize=(12, 8))  # Tamaño adecuado

    # Obtener pesos de aristas y normalizar
    edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
    weights = np.array(weights)
    
    # Mapa de colores para los pesos
    cmap = plt.cm.coolwarm  # Paleta de colores
    norm = plt.Normalize(vmin=0, vmax=1)  # Normalización del rango

    # Dibujar nodos con colores según el componente conexo
    components = list(nx.connected_components(G))
    colors = plt.cm.tab20(range(len(components)))  # Diferentes colores por componente

    for component, color in zip(components, colors):
        nx.draw_networkx_nodes(G, pos, nodelist=component, node_color=[color], node_size=700)

    # Dibujar aristas con color y grosor según el peso
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=weights, edge_cmap=cmap, width=weights * 5, edge_vmin=0, edge_vmax=1)

    # Dibujar etiquetas de nodos
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Agregar barra de colores
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm)
    cbar.set_label("Peso de las aristas")

    plt.title("Visualización del Grafo con Pesos de Aristas")
    plt.axis('off')  # Ocultar ejes
    plt.show()

def simulate_coincidence(m,s):
    #random.seed(1751751)
    G=nx.Graph()
    primera_linea = True
    with open(NOMFITXER) as f:
        for linia in f:
            if primera_linea:   primera_linea=False
            else:
                coincidencia = random.gauss(m,s)
                print(coincidencia)
                if coincidencia > 1:        coincidencia = 1
                elif coincidencia < 0:      coincidencia = 0
                node1,node2 = linia.strip().split(",")
                print(node1,node2,coincidencia)
                G.add_weighted_edges_from(node1,node2,coincidencia)
                
    return G

Graf = simulate_coincidence(0.5, 0.25)
draw_graph(Graf)