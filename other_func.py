import networkx as nx
import random 
#Constructor de grafs a partir d'un fitxer d'arestes
def build_lastgraph(NomFitxer:str) -> nx.Graph:
    G=nx.Graph()
    primera_linea = True
    with open(NomFitxer) as f:
        for linia in f:
            if primera_linea:   primera_linea=False
            else:
                node1,node2 = linia.strip().split(",")
                G.add_edge(node1,node2)
    return G

print(random.gauss(10,2))
