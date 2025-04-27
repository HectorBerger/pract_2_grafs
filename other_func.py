import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time


###Other functions

#
def draw_graph(G: nx.Graph):
    pos = nx.spring_layout(G, seed=42, k=0.3)  # Mejor disposición

    plt.figure(figsize=(12, 8))  # Tamaño adecuado
    ax = plt.gca()  # Obtener el objeto Axes actual

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
        nx.draw_networkx_nodes(G, pos, nodelist=component, node_color=[color], node_size=700, ax=ax)

    # Dibujar aristas con color y grosor según el peso
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=weights, edge_cmap=cmap, width=weights * 5, edge_vmin=0, edge_vmax=1, ax=ax)

    # Dibujar etiquetas de nodos
    nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

    # Agregar barra de colores
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label("Peso de las aristas")

    plt.title("Visualización del Grafo con Pesos de Aristas")
    plt.axis('off')  # Ocultar ejes
    plt.show()

#Constructor de grafs a partir d'un fitxer d'arestes
def build_lastgraph(NomFitxer:str, num_i:int = 27808) -> nx.Graph:
    G=nx.Graph()
    i=0
    with open(NomFitxer) as f:
        for linia in f.readlines()[1:]:
            node1,node2 = linia.strip().split(",")
            G.add_edge(node1,node2)
            i+=1
            if i > num_i:
                break

    return G

#Funció Timer per calcular el temps d'execució d'una funció
def timer(func, nom_funcio: str, printejar: bool):
    def wrapper(*args, **kwargs): #wrapper per poder executar la funció amb els paràmetres passats (tants com siguin necessaris)
        start_time = time.time()
        resultat = func(*args, **kwargs)
        end_time = time.time()
        if printejar:
            print(f"Temps d'execució {nom_funcio}: {end_time - start_time} segons")
        return resultat, end_time - start_time #Retornarem el resultat de la funció i el temps que ha tardat en executar-se
    return wrapper