from networkx.algorithms import isomorphism
import  networkx as nx
from functions import analysis_function as af
from functions import graph_function as gf
from functions import substructure_algo as sa
import copy

def multiplicity_subtree(G, H):
    # Массивы поддеревьев
    subtrees_G = []
    subtrees_H = []
    G_graph = gf.transform_into_graph_algo(G)
    H_graph = gf.transform_into_graph_algo(H)

    # Нахождение всех поддеревьев
    for obj in G['children']:
        new_graph_g = copy.deepcopy(G_graph)
        sa.del_nodes(new_graph_g, obj, G)
        new_graph_g.remove_node(new_graph_g['_id'])
        subtrees_G.append(new_graph_g)

    for obj in H['children']:
        new_graph_h = copy.deepcopy(H_graph)
        sa.del_nodes(new_graph_h, obj, H)
        new_graph_h.remove_node(new_graph_h['_id'])
        subtrees_H.append(new_graph_h)

    for vertex_G in subtrees_G:
        for vertex_H in subtrees_H:
            

