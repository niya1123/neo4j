import sys

sys.path.append("/dic/neo4j")
import json
from collections import defaultdict
from connection_neo4j import ConnectNeo4j as CN
from create_MATCH_query import CreateMATCHQuery as CMQ
from create_node_and_relationship import CreateNodeAndRelationship as CNAR
from create_DELETE_query import CreateDELETEQuery as CDQ
from flask import Flask, jsonify, render_template, request, Response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def return_json(result):
    data = [record.data()['rel'] for record in result]
    # json_obj = "["
    json_obj = defaultdict(list)
    for d in data:
        # json_obj += "{"
        # json_obj += f'"parent":"{d[0]["name"]}","children":"{d[2]["name"]}","relationship":"{d[1]}"'
        # json_obj += "},"
        json_obj['parent'].append(d[0]['name'])
        json_obj['children'].append(d[2]['name'])
        json_obj['relationship'].append(d[1])
    # json_obj += "]"
    # print(json_obj)
    json_obj = json.dumps(json_obj, ensure_ascii=False, default=str)
    res = Response(json_obj,content_type='application/json; charset=utf-8')
    # res.headers.add('content-length',len(res))
    res.status_code=200
    return res

def return_score_json(username,result):
    pass

@app.route('/', methods=["GET"])
def main():
    return render_template("main.html")

@app.route('/', methods=["POST"])
def main_post():
    node1 = request.form["node1"]
    node2 = request.form["node2"]
    relationship = request.form["relationship"]
    cnar = CNAR()
    cnar.create_Node(node_name=node1)
    cnar.create_Node(node_name=node2)
    cnar.create_relationship(node1, node2, relationship)
    cnar.close()
    cn = CN()
    session = cn.get_session()
    result =session.run(CMQ._create_MATCH_query(node1_name=node1, node2_name=node2, relationship=relationship))
    res = return_json(result)
    cn.close()
    return  jsonify(res)

@app.route('/create/score', methods=["GET"])
def create_score():
    return render_template("score.html")

@app.route('/create/score', methods=["POST"])
def post_create_score():
    node1 = request.form["node1"]
    node2 = request.form["node2"]
    score = request.form["score"]
    cnar = CNAR()
    cnar.create_Node(node_name=node1)
    cnar.create_Node(node_name=node2)
    cnar.create_score(node1, node2, score)
    cnar.close()
    return  "登録しました"

@app.route('/get/all_graphs', methods=["GET"])
def get_all_graph():
    """
    全てのグラフデータのノードと関係性を返す関数. 
    """
    cn = CN()
    session = cn.get_session()
    result = session.run(CMQ._create_MATCH_query())
    res = return_json(result)
    cn.close()
    return res

@app.route('/get/score', methods=["POST"])
def get_score_graph():
    """
    特定人物が受験した科目と点数を返す関数. 
    """
    username = request.form["username"]
    cn = CN()
    session = cn.get_session()
    result = session.run(CMQ._create_MATCH_userscore_query(username))
    res = return_json(username,result)
    cn.close()
    return res

@app.route('/create/json', methods=["POST"])
def post_node_and_relationship():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400

    json_data = request.json
    json_data_len = len(json_data)
    type = json_data[0]['text']
    parent_data = []
    child_data = []
    for i in range(json_data_len):
        parent_id = json_data[i]['parent']
        if parent_id == "type":
           parent_data.append({'type': type, 'node_name': json_data[i]['text'], 'id': json_data[i]['id']})
        elif parent_id == "parent":
            child_data.append({'type': type, 'node_name': json_data[i]['text'], 'parent_id': "parent"})
        else:
            if parent_id in [parent['id'] for parent in parent_data]:
                child_data.append({'type': type, 'node_name': json_data[i]['text'], 'parent_id': parent_id})
    result = [parent['node_name'] + '-' + child['node_name'] for parent in parent_data for child in child_data if parent['id'] == child['parent_id']]
    for r in result:
        node1, node2 = tuple(filter(None, r.split('-')))
        relationship = 'have'
        create_node_and_relationship_with_type(node1, node2, relationship, type)
   
    return jsonify(res='ok')

def create_node_and_relationship(node1, node2, relationship):
    cnar = CNAR()
    cnar.create_Node(node_name=node1)
    cnar.create_Node(node_name=node2)
    cnar.create_relationship(node1, node2, relationship)
    cnar.close()
    cn = CN()
    session = cn.get_session()
    result = session.run(CMQ._create_MATCH_query(node1_name=node1, node2_name=node2, relationship=relationship))
    # res = return_json(result)
    cn.close()
    return  jsonify(res='200')

def create_node_and_relationship_with_type(node1, node2, relationship, type):
    cnar = CNAR()
    cnar.create_Node(node_name=node1, type=type)
    cnar.create_Node(node_name=node2, type=type)
    cnar.create_relationship(node1, node2, relationship)
    cnar.close()
    cn = CN()
    session = cn.get_session()
    result = session.run(CMQ._create_MATCH_query(node1_name=node1, node2_name=node2, relationship=relationship))
    # res = return_json(result)
    cn.close()
    return  jsonify(res='200')

@app.route('/delete/<string:node_name>', methods=["GET"])
def delete_node(node_name):
    cdq = CDQ(CN().driver)
    cdq.run_DELETE(node_name=node_name)
    cdq.close()
    return "{}を削除しました.".format(node_name)

@app.route('/delete/all', methods=["GET"])
def delete_all_node():
    cdq = CDQ(CN().driver)
    cdq.run_DELETE()
    cdq.close()
    return "すべてのノードを削除しました"

@app.route('/create/json', methods=["GET"])
def create_json():
    return render_template("create_json.html")

@app.route('/cytoscape', methods=["GET"])
def cytoscape():
    return render_template("cytoscape.html")

@app.route('/get/score', methods=["GET"])
def get_score():
    cn = CN()
    cmq = CMQ(cn.driver)
    query = cmq._create_MATCH_score_query()
    result = cn.get_session().run(query)
    # res = return_json(result)
    cn.close()
    return jsonify(res="200")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7878, debug=True)
