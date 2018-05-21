import json
import requests
from requests.auth import HTTPBasicAuth
import webbrowser
import copy
import flask
from openpyxl import load_workbook
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
from functions import analysis_function as af
from functions import substructure_algo as sub_algo
from functions import graph_function as gf
from functions import subtree_isomorphism as si


app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if coggle_user.access_token == "":
        coggle_user.authorization_token()
    if request.method == 'POST':
        if 'file_input' not in request.files:
            flask.flash('No file part', 'input')
            return redirect(request.url)

        file = request.files['file_input']
        #file_ref = request.files['files_input_ref']
        form = request.form['form_algo']

        if file.filename == '':
            flask.flash('No selected file', 'input')
            return redirect(request.url)
        #if file_ref.filename == '':
        #    flask.flash('Вы не выбрали файл!', 'input_ref')
        #    return redirect(request.url)

        if file:
            filename_file = secure_filename(file.filename)
            file.save(filename_file)
            if form == "without_ref":
                take_mm(filename_file)
            elif form == "with_ref":
                take_mm(filename_file, True)
            return redirect(request.url)
    return render_template('index.html')


def take_mm(filename, status = None):
    wb = load_workbook(filename=filename)
    sheet = wb[wb.sheetnames[0]]
    id_diagram_1 = sheet['A1'].value
    id_diagram_2 = sheet['A2'].value
    if status is None:
        arr = []
        arr.append(information_for_algo(id_diagram_1))
        arr.append(information_for_algo(id_diagram_2))

        arr_ids = gf.read_mm_ids(sheet, "B")
        n = len(arr_ids)
        mass = [[0] * 2 for i in range(n)]
        for i in range(0, len(arr_ids)):
            for j in range(0, 2):
                curr_map = information_for_algo(arr_ids[i])
                mass[i][j] = si.max_common_substree_rooted(arr[j]['diagram'], curr_map['diagram'])
                '''
                curr_map = information_for_algo(arr_ids[i])
                new_graph = copy.deepcopy(arr[j]['graph'])
                algo = sub_algo.max_comp_element(arr[j]['diagram'], new_graph, curr_map['graph'])
                last_graph = gf.create_graph_form_list(algo)
                mass[i][j] = af.similarity_sub_algo(last_graph, arr[j]['graph'], curr_map['graph'])
                '''
        shod = si.max_common_substree_rooted(arr[0]['diagram'], arr[1]['diagram'])
        output_sheet = wb.create_sheet('matrix')
        gf.print_matrix(output_sheet, mass)
        wb.save(filename)
        '''
        new_graph = copy.deepcopy(arr[0]['graph'])
        algo = sub_algo.max_comp_element(arr[0]['diagram'], new_graph, arr[1]['graph'])
        last_graph = gf.create_graph_form_list(algo)
        qweqwe = af.similarity_sub_algo(last_graph, arr[0]['graph'], arr[1]['graph'])
        '''

    else:
        arr_ids = gf.read_mm_ids(sheet, "B")
        n = len(arr_ids)
        mass = [[0] * n for i in range(n)]
        for i in range(0, len(arr_ids)):
            for j in range(0, len(arr_ids)):
                mind_map_1 = coggle_user.diagram(arr_ids[i])
                mind_map_2 = coggle_user.diagram(arr_ids[j])
                mass[i][j] = si.max_common_substree_rooted(mind_map_1, mind_map_2)
                '''
                mind_map_1 = information_for_algo(arr_ids[i])
                mind_map_2 = information_for_algo(arr_ids[j])
                new_graph_1 = copy.deepcopy(mind_map_1['graph'])
                algo = sub_algo.max_comp_element(mind_map_1['diagram'], new_graph_1, mind_map_2['graph'])
                last_graph = gf.create_graph_form_list(algo)
                mass[i][j] = af.similarity_sub_algo(last_graph, mind_map_1['graph'], mind_map_2['graph'])
                '''
        output_sheet = wb.create_sheet('matrix')
        gf.print_matrix(output_sheet, mass)
        wb.save(filename)
'''
# mind_map_1 = information_for_algo(id_diagram_1)
        # mind_map_2 = information_for_algo(id_diagram_2)
        new_graph_1 = copy.deepcopy(mind_map_1['graph'])

        algo = sub_algo.max_comp_element(mind_map_1['diagram'], new_graph_1, mind_map_2['graph'])
        last_graph = gf.create_graph_form_list(algo)
        procent = af.similarity_sub_algo(last_graph, mind_map_1['graph'], mind_map_2['graph'])

        output_sheet = wb.create_sheet('output')
        output_sheet['A1'] = "Мера сходства"
        output_sheet['A2'] = procent
        gf.print_metrics(output_sheet, af.metrics(mind_map_1['diagram'], mind_map_1['graph']), af.metrics(mind_map_2['diagram'], mind_map_2['graph']))
        wb.save(filename)
'''


def information_for_algo(id_diagram):
    arr = {'diagram': '', 'graph': ''}
    arr['diagram'] = coggle_user.nodes(id_diagram)
    arr['graph'] = gf.transform_into_graph(arr['diagram'])
    return arr


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
        app.run()

    def authorization_token(self):
        code = request.args.get('code')
        params = {"code": code, "grant_type": "authorization_code", "redirect_uri": self.redirect_uri}
        resp1 = requests.post(self.url_base + "token", auth=HTTPBasicAuth(client_id, self.client_secret), json=params)
        information_auth = json.loads(resp1.text)
        self.access_token = information_auth["access_token"]

    # Получение информации о всей диаграмме
    def diagram(self, id_diagram):
        params = {"access_token": self.access_token}
        url_diagram = "api/1/diagrams/"
        information_diagram = requests.get(self.url_base + url_diagram + id_diagram, params=params)
        diagram = json.loads(information_diagram.text)
        return diagram

    # Получение информации о вершинах
    def nodes(self, id_diagram):
        params = {"access_token": self.access_token}
        url_diagram = "api/1/diagrams/"
        information_nodes = requests.get(self.url_base + url_diagram + id_diagram + "/nodes", params=params)
        nodes = json.loads(information_nodes.text)
        return nodes


# Информация пользователя
app_name = "CourseWork"
client_id = "5a8ab7821c5b5b00010853f0"
client_secret = "52cc11494efb7b38cbcfd113fc8f6f67b0d09c5aaccce7a07f2a6c177a34c772"
redirect_uri = "http://localhost:5000"

coggle_user = Coggle(app_name, client_id, client_secret, redirect_uri)
coggle_user.authorization()

