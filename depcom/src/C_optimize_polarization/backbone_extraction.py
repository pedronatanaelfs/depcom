import networkx as nx
import numpy as np

def disparity_filter(G, alpha_threshold=0.05):
    """
    Aplica o filtro de disparidade para extrair o backbone do grafo.
    
    Args:
        G (networkx.Graph): Grafo de entrada.
        alpha_threshold (float): Valor de alpha para remover arestas. Default é 0.05.
    
    Retorna:
        networkx.Graph: Grafo contendo apenas o backbone.
    """
    # Cria um grafo vazio para armazenar o backbone
    G_backbone = nx.Graph()
    G_backbone.add_nodes_from(G.nodes(data=True))

    # Itera sobre cada nó do grafo original
    for node in G.nodes():
        # Obtém o grau do nó
        k = len(G[node])
        if k < 2:
            continue  # O filtro de disparidade não é aplicável para nós com grau menor que 2

        # Calcula a soma total dos pesos das arestas incidentes ao nó
        total_weight = sum(G[node][neighbor]['weight'] for neighbor in G[node])

        # Aplica o filtro de disparidade em cada aresta
        for neighbor in G[node]:
            weight = G[node][neighbor]['weight']
            p_ij = weight / total_weight

            # Calcula o valor de alpha_ij
            alpha_ij = 1 - (k - 1) * (1 - p_ij)**(k - 2)

            # Mantém a aresta no backbone se alpha_ij for menor que o threshold
            if alpha_ij < alpha_threshold:
                G_backbone.add_edge(node, neighbor, weight=weight)

    return G_backbone
