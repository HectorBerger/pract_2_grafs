#Prac_2
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time

#Simulació
NOMFITXER = "lastfm_asia_edges.csv" #graf_petit.csv lastfm_asia_edges.csv

#Other functions
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
def timer(func, nom_funcio: str):
    def wrapper(*args, **kwargs): #wrapper per poder executar la funció amb els paràmetres passats (tants com siguin necessaris)
        start_time = time.time()
        resultat = func(*args, **kwargs)
        end_time = time.time()
        print(f"Temps d'execució {nom_funcio}: {end_time - start_time} segons")
        return resultat #Retornarem el resultat de la funció i el temps que ha tardat en executar-se
    return wrapper

#1
def simulate_coincidence(m,s):
    #random.seed(1751751)
    G=nx.Graph()
    with open(NOMFITXER) as f:
        for linia in f.readlines()[1:]:
            coincidencia = random.gauss(m,s)
            if coincidencia > 1:        
                coincidencia = 1
            elif coincidencia < 0:      
                coincidencia = 0
            node1,node2 = linia.strip().split(",")
            G.add_weighted_edges_from([(node1,node2,coincidencia)])       
    return G

def how_many_cliques(n,m,s):
    G = simulate_coincidence(m,s)
    
    # Filtrar aristas con peso mayor que n
    filtered_edges = [(u, v) for u, v, data in G.edges(data=True) if data['weight'] > n]
    G_filtered = nx.Graph(filtered_edges)

    # Encontrar todos los cliques
    cliques = list(nx.find_cliques(G_filtered))

    # Contar cliques por tamaño
    clique_counts = {}
    for clique in cliques:
        size = len(clique)
        if size not in clique_counts:
            clique_counts[size] = 0
        clique_counts[size] += 1

    # Imprimir resultados
    for size in sorted(clique_counts.keys()):
        print(f"Número de cliques de tamaño {size}: {clique_counts[size]}")

#how_many_cliques(0.8,0.95,0.25)


#2
def loto():
    n = int(input("Introdueix quants números vols jugar: "))
    m = int(input("Introdueix el màxim de valors possibles: "))
    
    #NO FUNCIONA SI N > M . SE PUEDE ARREGLAR?
    print(f"Introdueix {n} números entre 1 i {m} separats per espais:")
    entrada = input("Els teus números: ") #HABRÍA QUE CONTROLAR EL INPUT (Que te vuelva a preguntar si lo has introducido mal)
    jugada = list(map(int, entrada.strip().split()))

    jugada = sorted(jugada)

    intents = 0

    while True:
        sorteig = random.sample(range(1, m + 1), n)
        intents += 1

        #print (f"El sorteig és: {sorteig}")

        if sorteig == jugada:
            print("has guanyat!")
            break
        
    print(f"Has necessitat {intents} intents per guanyar.")
    print(f"Els teus números són: {jugada}")

loto()


#3

#G = build_lastgraph(NOMFITXER,1000)
#d = timer(nx.coloring.greedy_color, "Greedy Color (largest_first)")(G, strategy='largest_first', interchange=False)
#print(d)
