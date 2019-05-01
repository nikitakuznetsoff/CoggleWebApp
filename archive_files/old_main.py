import json
import requests
from requests.auth import HTTPBasicAuth
import webbrowser
import networkx as nx
from networkx.algorithms import isomorphism
import matplotlib.pyplot as plt
import analysis_function as af
import substructure_algo as sub_algo
import graph_function as gf
import copy
import flask
from openpyxl import load_workbook
from flask import Flask, request, redirect
from werkzeug.utils import secure_filename
from flask import Flask


# Класс для основных операций с API
class Coggle:
    def __init__(self, app_name, client_id, client_secret, redirect_uri):
        self.app_name = app_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.url_base = "https://coggle.it/"
        self.access_token = ""

    # Авторизация
    def authorization(self):
        params = {'response_type': "code", 'scope': "read", 'client_id': self.client_id, 'redirect_uri': self.redirect_uri}
        resp_auth = requests.get(self.url_base + 'dialog/authorize/', params=params)
        webbrowser.open_new_tab(resp_auth.url)
        print("Код для авторизации")
        code = input()

        params = {"code": code, "grant_type": "authorization_code", "redirect_uri": self.redirect_uri}
        resp_token = requests.post(self.url_base + "token", auth=HTTPBasicAuth(client_id, self.client_secret), json=params)
        information_auth = json.loads(resp_token.text)
        self.access_token = information_auth["access_token"]
        if self.access_token != "":
            return True
        return False

    # Получение информации о всей диаграмме
    def diagram(self, id_diagram):
        params = {"access_token": self.access_token}
        url_diagram = "api/1/diagrams/"
        resp = requests.get(self.url_base + url_diagram + id_diagram, params=params)
        diagram = json.loads(resp.text)
        return diagram

    # Получение информации о вершинах
    def nodes(self, id_diagram):
        params = {"access_token": self.access_token}
        url_diagram = "api/1/diagrams/"
        resp = requests.get(self.url_base + url_diagram + id_diagram + "/nodes", params=params)
        nodes = json.loads(resp.text)
        return nodes


def metrics(nodes, graph):
    met = {"max_height": 0, "count_nodes": 0, "count_first_layer_branches": 0, "images": 0, "avg_node_text_len": 0}
    met["max_height"] = af.max_height(nodes)
    met["count_nodes"] = af.count_nodes(graph)
    met["count_first_layer_branches"] = af.count_first_layer_branches(nodes)
    met["images"] = af.images_count(nodes)
    met["avg_node_text_len"] = af.avg_node_text_len(nodes, met["count_nodes"])
    return met


# Информация пользователя
app_name = "CourseWork"
client_id = "5a8ab7821c5b5b00010853f0"
client_secret = "52cc11494efb7b38cbcfd113fc8f6f67b0d09c5aaccce7a07f2a6c177a34c772"
redirect_uri = "http://localhost:5000"

coggle_user = Coggle(app_name, client_id, client_secret, redirect_uri)

coggle_user.authorization()

# ИДшники диаграмм
    # ID для большой карты
id_diagram_1 = "WtPBgA68PdTIEORd"
    # ID для малой
id_diagram_2 = "WtyXD7KpvB1q33Vk"


diagram_1 = coggle_user.nodes(id_diagram_1)
diagram_2 = coggle_user.nodes(id_diagram_2)
graph_1 = gf.transform_into_graph(diagram_1)
graph_2 = gf.transform_into_graph(diagram_2)

print("Проверка на изоморфизм")
# Проверка на изоморфизм графов
em = isomorphism.categorical_edge_match('colour', '')
nm = isomorphism.categorical_node_match('text', '')
GM = isomorphism.DiGraphMatcher(graph_1, graph_2, node_match=nm, edge_match=em)
print(GM.subgraph_is_isomorphic())

print("Алгоритм подстркутурный")
graph_1_new = copy.deepcopy(graph_1)
algo = sub_algo.max_comp_element(diagram_1, graph_1_new, graph_2)

last_graph = nx.DiGraph()
for obj in algo:
    last_graph.add_nodes_from(obj.nodes())
    last_graph.add_edges_from(obj.edges())
shod = (af.count_nodes(last_graph) * af.count_nodes(last_graph)) / (af.count_nodes(graph_1) * af.count_nodes(graph_2))
print(shod)

nx.draw(last_graph)
plt.show()
print("Метрики")
print(metrics(diagram_1, graph_1))
