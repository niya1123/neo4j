import sys

sys.path.append("/dic/neo4j")
import json

from connection_neo4j import ConnectNeo4j as CN
from create_MATCH_query import CreateMATCHQuery as CMQ
from create_node_and_relationship import CreateNodeAndRelationship as CNAR
from create_DELETE_query import CreateDELETEQuery as CDQ
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def return_json(result):
    data = [record.data()['rel'] for record in result]
    json_obj = "{"
    for d in data:
        json_obj += f"['parent':'{d[0]['name']}','children':'{d[2]['name']}','relationship':'{d[1]}'],"
    json_obj += "}"
    res = json.dumps(json_obj, ensure_ascii=False)
    return res

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
    return jsonify(res)

@app.route('/post/create_node_and_relationship', methods=["POST"])
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
    res = return_json(result)
    cn.close()
    return  jsonify(res)

def create_node_and_relationship_with_type(node1, node2, relationship, type):
    cnar = CNAR()
    cnar.create_Node(node_name=node1, type=type)
    cnar.create_Node(node_name=node2, type=type)
    cnar.create_relationship(node1, node2, relationship)
    cnar.close()
    cn = CN()
    session = cn.get_session()
    result = session.run(CMQ._create_MATCH_query(node1_name=node1, node2_name=node2, relationship=relationship))
    res = return_json(result)
    cn.close()
    return  jsonify(res)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7878, debug=True)
