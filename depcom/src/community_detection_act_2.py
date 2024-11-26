# Import libraries
import networkx as nx
from cdlib import algorithms, evaluation, viz
import matplotlib.pyplot as plt

# Load the graph
graph_path = "depcom/src/graph_2023_communities.gml"
G = nx.read_gml(graph_path)

# 1. Applying two community detection algorithms
print("Detecting communities using Leiden...")
leiden_communities = algorithms.leiden(G)

print("Detecting communities using Infomap...")
infomap_communities = algorithms.infomap(G)

# 2. Evaluating communities using modularity
leiden_modularity = evaluation.newman_girvan_modularity(G, leiden_communities)
infomap_modularity = evaluation.newman_girvan_modularity(G, infomap_communities)

print(f"Modularity (Leiden): {leiden_modularity.score}")
print(f"Modularity (Infomap): {infomap_modularity.score}")

# 3. Hyperparameter tuning

# Leiden optimization
best_resolution = None
best_modularity = -1

# Testing custom resolutions
for resolution in [0.5, 1.0, 1.5, 2.0]:
    # Adjusting edge weights to simulate resolution
    for u, v, data in G.edges(data=True):
        data['weight'] = data.get('weight', 1) * resolution

    communities = algorithms.leiden(G)
    modularity = evaluation.newman_girvan_modularity(G, communities).score

    if modularity > best_modularity:
        best_modularity = modularity
        best_resolution = resolution

print(f"Best resolution (Leiden): {best_resolution}, Modularity: {best_modularity}")

# Infomap optimization example
best_modularity = -1
best_communities = None

# Example loop to adjust edge weights
for weight_multiplier in [1, 2, 3]:
    # Adjust edge weights
    for u, v, data in G.edges(data=True):
        data['weight'] = data.get('weight', 1) * weight_multiplier

    communities = algorithms.infomap(G)
    modularity = evaluation.newman_girvan_modularity(G, communities).score

    if modularity > best_modularity:
        best_modularity = modularity
        best_communities = communities

print(f"Best modularity with Infomap: {best_modularity}")
print(f"Number of communities: {len(best_communities.communities)}")

# 4. Community description

# Leiden
print(f"Leiden - Number of communities: {len(leiden_communities.communities)}")
print(f"Leiden - Community sizes: {[len(c) for c in leiden_communities.communities]}")

# Infomap
print(f"Infomap - Number of communities: {len(infomap_communities.communities)}")
print(f"Infomap - Community sizes: {[len(c) for c in infomap_communities.communities]}")

# Visualizing communities and saving images
print("Saving visualization for Leiden communities...")
viz.plot_network_clusters(G, leiden_communities)
plt.savefig("leiden_communities.png", dpi=300)
plt.close()

print("Saving visualization for Infomap communities...")
viz.plot_network_clusters(G, infomap_communities)
plt.savefig("infomap_communities.png", dpi=300)
plt.close()

print("Community visualizations saved as 'leiden_communities.png' and 'infomap_communities.png'.")
