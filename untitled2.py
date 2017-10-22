from flask import Flask
import Queue
import collections, csv
from model import *
from flask import render_template, request, url_for, redirect
import json
from flask import jsonify
app = Flask(__name__)
keyword = None

@app.route('/', methods=["GET","POST"])
def hello_world():
    #tasks = myTable().get_data()
    with open('/Users/qialiu/Documents/Insights/untitled2/my_doc.json') as json_data:
        json_table = json.load(json_data)
    #return jsonify(tasks)
    #print tasks
        return render_template('index.html', result = json_table)

@app.route('/search', methods=["POST"])
def search():
    key_word = request.form['word'].encode('ascii', 'ignore')
    nodes = {}
    nodes_id_name = {}
    with open("/Users/qialiu/Documents/Insights/untitled2/nodes.csv", "rb") as f:
        reader = csv.reader(f, delimiter=",")
        reader.next()
        for i, line in enumerate(reader):
            nodes[line[1].strip()] = [int(line[0]), line[2]]
            nodes_id_name[int(line[0])] = [line[1].strip(), line[2]]
    ## graphic_dic
    graph_dic = collections.defaultdict(list)
    n = len(nodes)
    for i in range(n):
        graph_dic[i] = []

    with open("/Users/qialiu/Documents/Insights/untitled2/graph.csv", "rb") as f:
        reader = csv.reader(f, delimiter=",")
        reader.next()
        for i, line in enumerate(reader):
            if line[1]:
                graph_dic[int(line[0])].append(int(line[1]))

    all_components = SearchComp(graph_dic, nodes).find_connected_cpn()
    node_info = nodes.get(key_word)
    # format all_component to dic

    res = []

    if node_info:
        node_id = node_info[0]

        for comp in all_components:
            if node_id in comp:
                res = comp
                #for item in comp:
                    #    res.append(nodes_id_name.get(item))
                break

    # dynamically display the results
    nodes_level_dic = collections.defaultdict(set)
    for k, v_list in nodes_id_name.items():
        if len(v_list) == 2:
            nodes_level_dic[v_list[1].strip()].add(k)

    def create_nested_dic(comp, nodes_level_dic):
        # input: comp, a list of nodes; graph_dic: the overall structure, nodes: the characters of nodes
        # 1st search component level node, if exist, then starting from them search next level nodes
        # 1. component, 2. role, 3. class, 4. attribute, 5. value
        component_level, role_level, class_level, attribute_level, value_level = None, None, None, None, None

        if nodes_level_dic.get("component"):
            print "test", comp, nodes_level_dic.get("component")
            component_level = set(comp).intersection(nodes_level_dic.get("component"))
        if nodes_level_dic.get("Role"):
            role_level = set(comp).intersection(nodes_level_dic.get("Role"))
        if nodes_level_dic.get("class"):
            class_level = set(comp).intersection(nodes_level_dic.get("class"))
        if nodes_level_dic.get("attribute"):
            attribute_level = set(comp).intersection(nodes_level_dic.get("attribute"))
        if nodes_level_dic.get("value"):
            value_level = set(comp).intersection(nodes_level_dic.get("value"))

        print component_level
        visited = set()

        # initialize root of the nested_dic
        nested_dic = {}
        nested_dic["root"] = []

        for cp in component_level:
            tmp_cp = {}
            tmp_cp["name"] = nodes_id_name[cp][0] + ": component"
            tmp_cp["sub"] = []
            edges = graph_dic.get(cp)
            for role in edges:
                if role_level and role in role_level:
                    tmp_role = {}
                    tmp_role["name"] = nodes_id_name[role][0] + ": role"
                    tmp_cp["sub"].append(tmp_role)
                elif class_level and role in class_level:
                    tmp_class = {}
                    tmp_class["name"] = nodes_id_name[role][0] + ": class"
                    tmp_class["sub"] = []
                    ## attribute level
                    class_edges = graph_dic.get(role)
                    for attr in class_edges:
                        if attribute_level and attr in attribute_level:
                            tmp_attr = {}
                            tmp_attr["name"] = nodes_id_name[attr][0] + ": attribute"
                            tmp_attr["sub"] = None
                            tmp_class["sub"].append(tmp_attr)
                    tmp_cp["sub"].append(tmp_class)

            nested_dic["root"].append(tmp_cp)

        f = json.dumps(nested_dic)
        return f

    json_res = create_nested_dic(res, nodes_level_dic)
    print json_res

    return render_template('search.html', json_res = json_res)

@app.route('/stats_res', methods=["POST"])
def stats_res():
    table  = []
    return render_template('search.html', table = table)


if __name__ == '__main__':
    app.run(debug=True)
