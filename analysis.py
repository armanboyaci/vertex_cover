# -*- coding: utf-8 -*-
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

import pandas as pd
import networkx as nx
from networkx.algorithms.approximation import min_weighted_vertex_cover
import matplotlib.pyplot as plt

with open('data/neighbor_cities_in_Turkey.txt', 'r') as f:
    lines = f.read().splitlines() 

G = nx.from_dict_of_lists({line.split(',')[0]: line.split(',')[1:] for line in lines})

len(set(G.nodes))

G.nodes

# + active=""
# for city in a.keys():
#     for c in a[city]:
#         print(c, city)
#         assert(city in a[c])
# -

#source: "https://simplemaps.com/data/tr-cities"
coordinates_and_population = pd.read_csv("data/coordinates.csv")[["city", "lng", "lat", 'population']]

coordinates_and_population.city = (coordinates_and_population.city
                                   .str.replace('ş','s')
                                   .str.replace('ğ','g')
                                   .str.replace('ı','i')
                                   .str.replace('ç','c')
                                   .str.replace('ü','u')
                                   .str.replace('Ş','S')
                                   .str.replace('ö','o')
                                   .str.replace('Ç','C')
                                   .str.replace('Ü','U')
                                   .str.replace('İ','I')
                                   .str.replace('Ö','O')
                                   .str.replace('Afyonkarahisar','Afyon'))

coordinates_and_population = coordinates_and_population.set_index('city')
coordinates_and_population = coordinates_and_population.loc[~coordinates_and_population.index.duplicated(keep='first')]
coordinates_and_population = coordinates_and_population.reindex(G.nodes)

len(coordinates_and_population)

pos = coordinates_and_population[["lng", "lat"]].T.to_dict(orient='list')

# +
#biggest_30_cities = coordinates_and_population.population.sort_values(ascending=False).head(30).index
# -

#source: https://www.haberturk.com/giris-cikis-yasaklanan-iller-hangisidir-30-buyuksehir-listesi-2020-2635405
restricted_cities = ["Adana", "Ankara", "Antalya", "Aydın", "Balıkesir", "Bursa", "Denizli", "Diyarbakır", 
 "Erzurum", "Eskişehir", "Gaziantep", "Hatay", "İstanbul", "İzmir", "Kahramanmaraş", 
 "Kayseri", "Kocaeli", "Konya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", 
 "Ordu", "Sakarya", "Samsun", "Şanlıurfa", "Tekirdağ", "Trabzon", "Van", "Zonguldak"]

restricted_cities = (pd.Series(restricted_cities)
 .str.replace('ş','s')
 .str.replace('ğ','g')
 .str.replace('ı','i')
 .str.replace('ç','c')
 .str.replace('ü','u')
 .str.replace('Ş','S')
 .str.replace('ö','o')
 .str.replace('Ç','C')
 .str.replace('Ü','U')
 .str.replace('İ','I')
 .str.replace('Ö','O')
 .str.replace('Afyonkarahisar','Afyon')).values

plt.figure(figsize=(18,8)) 
nodes = nx.draw_networkx_nodes(G, pos=pos, alpha=0.3, node_size=100, node_color='green')
big_cities = nx.draw_networkx_nodes(G, nodelist=restricted_cities, pos=pos, alpha=0.2, node_size=500, node_color='red')
labels = nx.draw_networkx_labels(G, pos=pos)
edges = nx.draw_networkx_edges(G, pos=pos, alpha=0.3)

# 2-approx. algorithm for min. vertex cover
len(min_weighted_vertex_cover(G))

# maximum matching number is a lower bound for the min. vertex cover number
len(nx.max_weight_matching(G))

# |V| = a minimal vertex cover + a maximal independent set
len(G.nodes) - len(nx.algorithms.mis.maximal_independent_set(G))

vertex_cover = set(G.nodes).difference(nx.algorithms.mis.maximal_independent_set(G))

plt.figure(figsize=(18,8)) 
nodes = nx.draw_networkx_nodes(G, pos=pos, alpha=0.3, node_size=100, node_color='green')
vc = nx.draw_networkx_nodes(G, nodelist=vertex_cover, pos=pos, alpha=0.2, node_size=500, node_color='blue')
labels = nx.draw_networkx_labels(G, pos=pos)
edges = nx.draw_networkx_edges(G, pos=pos, alpha=0.3)
