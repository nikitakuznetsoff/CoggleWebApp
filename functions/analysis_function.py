# Максимальное число ребер от корня
def max_height(nodes):
    arr = []
    if nodes:
        for obj in nodes:
            arr.append(max_height_children(obj))
        return max(arr)
    else:
        return 0


def max_height_children(nodes):
    if nodes['children']:
        arr = []
        for obj in nodes['children']:
            arr.append(max_height_children(obj))
        return max(arr) + 1
    else:
        return 0


# Количество вершин через networkx
def count_nodes(graph):
    return len(graph.nodes)


# Количество узлов от корневых вершин
def count_first_layer_branches(nodes):
    count = 0
    for obj in nodes:
        count += len(obj['children'])
    return count


# Количество изображений
def images_count(nodes):
    count = 0
    if nodes:
        for obj in nodes:
            if obj['text'].find(r"!\[([a-zA-Z0-9 ]*)\]\(https?:") != -1:
                count += obj['text'].count("![")
            count += images_count_children(obj)
    else:
        return 0
    return count


def images_count_children(nodes):
    count = 0
    for obj in nodes['children']:
        if obj['text'].find("![") != -1:
            count += obj['text'].count("![") + images_count_children(obj)
    return count


# Средняя длина текста
def avg_node_text_len(nodes, count_nodes):
    len_text = 0
    if nodes:
        for obj in nodes:
            if obj['text'].find("![") != -1:
                len_text += len(
                    obj['text'][0: obj['text'].find("![") - 2: 1]) + avg_node_text_len_children(obj)
            else:
                len_text += len(obj['text']) + avg_node_text_len_children(obj)
    else:
        return 0
    return len_text / count_nodes


def avg_node_text_len_children(nodes):
    len_text = 0
    if nodes['children']:
        for obj in nodes['children']:
            if obj['text'].find("![") != -1:
                len_text += len(
                    obj['text'][0: obj['text'].find("![") - 2: 1]) + avg_node_text_len_children(obj)
            else:
                len_text += len(obj['text']) + avg_node_text_len_children(obj)
    else:
        return 0
    return len_text


# Список метрик
def metrics(nodes, graph):
    met = {"max_height": 0, "count_nodes": 0, "count_first_layer_branches": 0, "images": 0, "avg_node_text_len": 0}
    met["max_height"] = max_height(nodes)
    met["count_nodes"] = count_nodes(graph)
    met["count_first_layer_branches"] = count_first_layer_branches(nodes)
    met["images"] = images_count(nodes)
    met["avg_node_text_len"] = avg_node_text_len(nodes, met["count_nodes"])
    return met


# Подсчет меры сходства для подструктурного подхода
def similarity_sub_algo(last_graph, graph_1, graph_2):
    return (count_nodes(last_graph) * count_nodes(last_graph)) / (count_nodes(graph_1) * count_nodes(graph_2))
