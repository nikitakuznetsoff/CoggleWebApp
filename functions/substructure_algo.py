from networkx.algorithms import isomorphism
from functions import analysis_function as af
from functions import graph_function as gf
import copy


# Метод для удаления ненужных поддеревьев в заданном дереве
def del_nodes(graph, obj_id, nodes):
    arr = []
    for obj in nodes['children']:
        if obj['_id'] != obj_id:
            arr.append(obj['_id'])
            del_nodes_rec(graph, obj['_id'], arr)
    graph.remove_nodes_from(arr)
    return graph


# Метод для рекурсивного вызова удаления вершин
def del_nodes_rec(graph, n, arr):
    for obj in graph.neighbors(n):
        arr.append(obj)
        del_nodes_rec(graph, obj, arr)


# Делает проход по корневым вершинам графа
def max_comp_element(nodes, graph, comp_graph):
    max_arr = []
    em = isomorphism.categorical_edge_match('colour', '')
    nm = isomorphism.categorical_node_match('text', '')
    GM = isomorphism.DiGraphMatcher(graph, comp_graph, node_match=nm, edge_match=em)
    if GM.subgraph_is_isomorphic():
        if af.count_nodes(graph) > af.count_nodes(comp_graph):
            max_arr.append(comp_graph)
            return max_arr
        else:
            max_arr.append(graph)
            return max_arr
    else:
        for obj in nodes:
            curr_graph = gf.transform_into_graph_algo(obj)
            max_comp_element_alg(obj, curr_graph, comp_graph, max_arr)
    return max_arr


# Рекурсивная часть алгоритма
def max_comp_element_alg(nodes, graph, comp_graph, max_arr):
    em = isomorphism.categorical_edge_match('colour', '')
    nm = isomorphism.categorical_node_match('text', '')
    GM = isomorphism.DiGraphMatcher(comp_graph, graph, node_match=nm, edge_match=em)
    if GM.subgraph_is_isomorphic():
        max_arr.append(graph)
    else:
        for obj in nodes['children']:
            new_graph = copy.deepcopy(graph)
            curr_graph = del_nodes(new_graph, obj['_id'], nodes)
            em = isomorphism.categorical_edge_match('colour', '')
            nm = isomorphism.categorical_node_match('text', '')
            GM = isomorphism.DiGraphMatcher(comp_graph, curr_graph, node_match=nm, edge_match=em)
            if GM.subgraph_is_isomorphic():
                max_arr.append(curr_graph)
            else:
                curr_graph.remove_edge(nodes['_id'], obj['_id'])
                curr_graph.remove_node(nodes['_id'])
                max_comp_element_alg(obj, curr_graph, comp_graph, max_arr)