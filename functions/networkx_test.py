import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import isomorphism
from networkx.algorithms import bipartite

B = nx.Graph()
B.add_nodes_from([1,2], bipartite=0)
B.add_nodes_from(['a','b','c'], bipartite=1)
B.add_edges_from([(1,'a'), (1,'b'), (2,'b'), (2,'a'), (2, 'c')])
B[1]['a']['weight'] = 2
B[1]['b']['weight'] = 2
B[2]['a']['weight'] = 2
B[2]['b']['weight'] = 2
B[2]['c']['weight'] = 2

print(nx.maximum_flow_value(B, 1, 'a', capacity='weight'))
flow_value, flow_dict = nx.maximum_flow(B, 1, 'c', capacity='weight')



Graph = nx.DiGraph()
Graph.add_nodes_from([1, 2, 3, 4])
Graph.add_edge(1, 2, weight=2)
Graph.add_edge(2, 3)
Graph[2][3]['weight'] = Graph[1][2]['weight']



print(list(Graph.neighbors(1)))
print(list(Graph.successors(1)))
print("...")
#print(nx.shortest_path(Graph, source=4, target=3))
#qweqwe = nx.DiGraph()
#qweqwe.add_nodes_from(nx.shortest_path(Graph, source=4, target=3))

G = nx.Graph()
# Вершины
G.add_node(1)
# Добавление вершин из списка
G.add_nodes_from([2, 3])
# Пучок вершин
H = nx.path_graph(10)
# Добавить вершины из H в G
G.add_nodes_from(H)
# Использовать граф H, как вершину в G
G.add_node(H)

# Ребра
G.add_edge(1, 2)
e = (1, 2)
G.add_edge(*e)
# add from list
G.add_edges_from([(1, 2), (1, 3)])
G.add_edges_from(H.edges())

# delete
# G.remove_node(H)
# G.remove_nodes_from(H)
# G.remove_edge(H)
# G.remove_edges_from(H)

###
G.clear()
G.add_edges_from([(1, 2), (1, 3)])
G.add_node(4)
G.add_node("spam")
G.add_nodes_from("spam")
print(G.number_of_edges())
print(G.number_of_nodes())

print(G.nodes())
print(G.edges())
print("tut")
print(list(G.neighbors('spam')))
print("tut")

print()
G.remove_nodes_from("spam")
print(G.nodes())
G.remove_edge(1, 3)
print(G.edges())

print()
H = nx.DiGraph(G)
print(H.edges())
H.clear()
edgelist = [(0, 1), (1, 2), (2, 3)]
H = nx.DiGraph(edgelist)
print(H.edges())

G[1][2]['color'] = 'blue'
print(G[1][2])
G[1][2]['color'] = 'red'
print(G[1][2])

###
FG = nx.Graph()
FG.add_weighted_edges_from([(1, 2, 0.4), (1, 3, 0.4), (2, 3, 0.4)])
print()
for (a, b, c) in FG.edges(data='weight'):
    if c < 0.5: print('(%d, %d, %.3f)' % (a, b, c))

###
print()
G.clear()
G = nx.Graph(day="Friday")
print(G.graph)

G.add_node(1, time='5pm')
print(G.node[1])
G.node[1]['room'] = 700
print('loh')
print(G.nodes[1])
print()

G.add_edge(1, 2, weight=4.5)
print(G[1][2])
G.add_edges_from([(3, 4), (4, 5)], color='red')
print(G[3][4], G[4][5])
G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight': 2.2})])
print()
print(G[1][2], G[2][3])

###
print()
DG = nx.DiGraph()
DG.add_weighted_edges_from([(1, 2, 0.5), (3, 1, 0.2)])
print(DG.out_degree(1, weight='weight'))
print(DG.degree(1, weight='weight'))
DG.successors(1)
print("qwe")
print(list(DG.neighbors(1)))
print("...")

#M = nx.read_graphml("file2.graphml")
#nx.draw(M)
#plt.show()
#print(M.edges())
#print(M.nodes(data=True))
#print(M.node['1aa42b381ab47751db9a6a78ce2a72ea'])

'''
Z = nx.parse_adjlist('start.graphml')
nx.draw(Z)
plt.show(Z)
'''

A = nx.Graph()
B = nx.Graph()

A.add_nodes_from([1, 2])
B.add_nodes_from([3, 4])

A.add_edge(1, 2)
B.add_edge(3, 4)

GM = isomorphism.GraphMatcher(A, B)
print(GM.is_isomorphic())