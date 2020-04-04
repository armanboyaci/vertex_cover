# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.1
#   kernelspec:
#     display_name: vertexcover
#     language: python
#     name: vertexcover
# ---

import networkx as nx
from networkx.algorithms.approximation import min_weighted_vertex_cover
import matplotlib.pyplot as plt

with open('data/neighbor_cities_in_Turkey.txt', 'r') as f:
    lines = f.read().splitlines() 

a = { line.split(',')[0]: line.split(',')[1:]  for line in lines}    

G = nx.from_dict_of_lists(a)

nx.draw(G)

len(G)

len(min_weighted_vertex_cover(G))

len(nx.max_weight_matching(G))

nx.planar_layout(G)

(_, H) = nx.algorithms.check_planarity(G, counterexample=True)

plt.figure(figsize=(12,8)) 
pos = nx.spring_layout(H, scale=2)
nodes = nx.draw_networkx_nodes(H, pos=pos)
labels = nx.draw_networkx_labels(H, pos=pos)
edges = nx.draw_networkx_edges(H, pos=pos)

S = [node for node, value in H.degree if H.degree[node] > 2]

H_prime = H.subgraph(S)

plt.figure(figsize=(12,4)) 
pos = nx.circular_layout(H_prime)
nodes = nx.draw_networkx_nodes(H_prime, pos=pos)
labels = nx.draw_networkx_labels(H_prime, pos=pos)
edges = nx.draw_networkx_edges(H_prime, pos=pos)
