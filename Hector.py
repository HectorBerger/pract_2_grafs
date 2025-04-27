#Pràctica_2
import networkx as nx
from networkx.algorithms import clique
import random
from other_func import draw_graph, build_lastgraph, timer

NOMFITXER = "lastfm_asia_edges.csv" #graf_petit.csv lastfm_asia_edges.csv


##1 - Simulació - Cliques
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

def how_many_cliques(n, m, s):
    G = simulate_coincidence(m, s)

    # Filtrar per llindar n
    Gf = nx.Graph( [(u, v) for u, v, d in G.edges(data=True) if d['weight'] > n] )

    # Enumerar tots els cliques
    all_cliques = list(clique.enumerate_all_cliques(Gf))

    # Comptar per mida
    counts = {}
    for C in all_cliques:
        k = len(C)
        counts[k] = counts.get(k, 0) + 1

    # Mostrar resultats
    for k in sorted(counts):
        print(f"Nombre de cliques de mida {k}: {counts[k]}")

"""
proves = [[0.1, 0.5, 0.25], [0.2, 0.5, 0.25], [0.5, 0.5, 0.25], [0.7, 0.5, 0.25], [0.8, 0.5, 0.25], [0.95, 0.5, 0.35], [1, 0.5, 0.25]] # Proves on només varia n (el nombre llindar de conexió) 
#proves = [[0.95, 0.1, 0.25], [0.95, 0.25, 0.25], [0.95, 0.5, 0.25], [0.95, 0.75, 0.25], [0.95, 1, 0.25]] #Proves per comprovar l'impacte de variar m (mitjana) amb els altres valors fixes
#proves = [[0.95, 0.5, 0], [0.95, 0.5, 0.1], [0.95, 0.5, 0.25], [0.95, 0.5, 0.5], [0.95, 0.5, 1], [0.95, 0.5, 4], [0.95, 0.5, 100]] #Proves per veure l'efecte de variar s (desviació típica) amb valor de n=0.95 i m=0.5
#proves = [[0.8, 0.5, 0.1], [0.1,0,0.05], [0.8,1,100], [0.95,0.5,0.5]] #Altres proves que hem utilitzat també
for i,p in enumerate(proves):
    print(f"\nProva {i}")
    timer(how_many_cliques, f"How many cliques? Provas {i}", True)(p[0], p[1], p[2]) #n = p[0], m = p[1], s = p[2] 
"""

##2 - La loto n<m
def loto() -> bool:
    n = int(input("Introdueix quants números vols jugar: "))
    m = int(input("Introdueix el màxim de valors possibles: "))

    if n > m:
        print(f"Error: No pots triar {n} números diferents entre 1 i {m}.")
        return False

    correcte = False
    while not correcte:
        print(f"Introdueix {n} números entre 1 i {m} separats per espais:")
        entrada = input("Els teus números: ")
        try:
            jugada = list(map(int, entrada.strip().split()))
            if len(jugada) != n:
                print("Error: has introduït un nombre incorrecte de números.")
            elif any(num < 1 or num > m for num in jugada):
                print(f"Error: Tots els números han d'estar entre 1 i {m}.")
            elif len(set(jugada)) != n:
                print("Error: Els números no poden estar repetits.")
            else:
                correcte = True
        except ValueError:
            print("Error: Has d'introduir números vàlids.")

    jugada = sorted(jugada)
    intents = 0

    while True:
        sorteig = random.sample(range(1, m + 1), n)
        intents += 1

        if sorted(sorteig) == jugada:
            print("Has guanyat!")
            break
        
    print(f"Has necessitat {intents} intents per guanyar.")
    print(f"Els teus números són: {jugada}")

    return True

#timer(loto, "Loteria", True)()


##3 - Els Problemes de Coloració són NP-complets
G = build_lastgraph(NOMFITXER)

arestes = list(G.edges())

estrategies = ['largest_first', 'random_sequential', 'smallest_last', 'independent_set', 'connected_sequential_bfs', 'connected_sequential_dfs', 'saturation_largest_first']
num_arestes = [100, 300, 500, 1000, 3000, 5000, 7500, 10000, 15000, 27806]

for estrategia in estrategies:
    print("\nEstrategia:", estrategia)
    for n in num_arestes:
        # Crear subgraf amb les primeres n arestes
        subgraf = nx.Graph()
        subgraf.add_edges_from(arestes[:n])

        # Aplicar greedy_color i mesurar temps amb timer
        coloracio, temps = timer(nx.coloring.greedy_color, "estrategia", False)(subgraf, strategy=estrategia)

        colors_usats = max(coloracio.values()) + 1  # +1 perquè els colors comencen a 0

        print("Arestes:", n, "Colors:", colors_usats, "Temps:", temps)
