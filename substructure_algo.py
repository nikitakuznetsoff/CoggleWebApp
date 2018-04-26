from networkx.algorithms import isomorphism
import analysis_function as af
import  networkx as nx
import graph_function as gf
import copy


def del_nodes(graph, obj_id, nodes):
    arr = []
    for obj in nodes['children']:
        if obj['_id'] != obj_id:
            arr.append(obj['_id'])
            rec_del(graph, obj['_id'], arr)
    graph.remove_nodes_from(arr)
    return graph


def rec_del(graph, n, arr):
    for obj in graph.neighbors(n):
        arr.append(obj)
        rec_del(graph, obj, arr)


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

'''
def max_comp_element_alg(nodes, comp_graph, max_arr):
    for obj in nodes['children']:
        new_nodes = copy.copy(nodes)
        qwe = gf.transform_into_graph_algo(nodes)
        with_del_nodes = delete_edges(new_nodes, obj)

        curr_graph = gf.transform_into_graph_algo(with_del_nodes)
        GM = isomorphism.GraphMatcher(curr_graph, comp_graph)
        if GM.is_isomorphic():
            max_arr.append(curr_graph)
        else:
            max_comp_element_alg(obj, comp_graph, max_arr)
    return
'''

'''
em = isomorphism.categorical_edge_match('colour', '')
nm = isomorphism.categorical_node_match('text', '')

GM = nx.is_isomorphic(graph, comp_graph, node_match=nm, edge_match=em)

    if not GM.is_isomorphic():
graph.remove_node(obj['_id'])
new_graph = graph.copy()
max_comp_element_alg(obj, new_graph, comp_graph)
return graph
'''

'''
for obj in nodes:
GM = isomorphism.DiGraphMatcher(graph, comp_graph)
if GM.is_isomorphic():
max_arr.append(graph)
else:
graph.remove_node(obj['_id'])
new_graph = graph.copy()
max_arr.append(max_comp_element_children(obj, new_graph, comp_graph))
return max_arr
'''