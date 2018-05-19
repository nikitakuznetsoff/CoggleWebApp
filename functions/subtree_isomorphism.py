from networkx.algorithms import isomorphism
import  networkx as nx
from functions import analysis_function as af
from functions import graph_function as gf
from functions import substructure_algo as sa
import copy

# Делаем поддерево от заданной точки
def subtree_by_node(graph, curr_node):
    new_graph = nx.DiGraph()
    new_graph.add_node(curr_node)
    for node in graph.neighbors(curr_node):
        new_graph.add_node(node)
        new_graph.add_edge(curr_node, node)
        subtree_by_node_rec(graph, node, new_graph)
    return new_graph


def subtree_by_node_rec(graph, curr_node, new_graph):
    for node in graph.neighbors(curr_node):
        new_graph.add_node(node)
        new_graph.add_edge(curr_node, node)
        subtree_by_node_rec(graph, node, new_graph)


# Создание графа от заднного корня до конкретной вершины
def make_graph(graph, root, node):
    list_nodes = nx.shortest_path(graph, source=root, target=node)
    new_graph = nx.DiGraph()
    new_graph.add_nodes_from(list_nodes)
    curr_node = graph[graph.node[root['_id']]]
    for obj in new_graph.nodes():
        if obj == curr_node:
            continue
        # obj = graph[obj]
        new_graph.add_edge(curr_node, obj)
        curr_node = obj
        # new_graph[curr_node][obj]['colour'] = graph[curr_node][obj]['colour']
    return new_graph


# Поиск максимального весового сравнения (MWM) в заданной матрице
def max_mwm(arr):

    return 0


# Поиск максимального общего дерева
def max_common_substree(G, H):
    gm_one = isomorphism.DiGraphMatcher(G, H)
    gm_two = isomorphism.DiGraphMatcher(H, G)
    return 0


# Основной алгоритм
def multiplicity_subtree(G, H):
    G_graph = gf.transform_into_graph(G)
    H_graph = gf.transform_into_graph(H)

    nodes_of_G = G_graph.nodes()
    nodes_of_G.remove(G['_id'])
    D = []

    for node_G in nodes_of_G:
        for node_H in H_graph.nodes():
            arr_of_node = list(H_graph.neighbors(node_H))
            arr_of_node.append(node_H)
            for s in arr_of_node:
                arr = []
                for u in G_graph.neighbors(node_G):
                    graph_form_root_G = make_graph(G_graph, node_G, u)
                    node_substree_G = subtree_by_node(G_graph, u)
                    arr.append([])
                    i = 0
                    for v in H_graph.neighbors(node_H):
                        graph_form_root_H = make_graph(H_graph, node_H, v)
                        node_substree_H = subtree_by_node(H_graph, v)
                        summ = max_common_substree(graph_form_root_G, graph_form_root_H) \
                               + max_common_substree(node_substree_G, node_substree_H)
                        arr[i].append(summ)
                        i += 1
                graph_form_root_r = make_graph(G_graph, G_graph[G['_id']], node_G)
                graph_form_root_s = make_graph(H_graph, node_H, s)
                D.append(max_common_substree(graph_form_root_r, graph_form_root_s) + max_mwm(arr))
'''
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

'''



