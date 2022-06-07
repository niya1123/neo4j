from crypt import methods
from email import message
import sys

sys.path.append("/dic/neo4j")
import json

from connection_neo4j import ConnectNeo4j as CN
from create_MATCH_query import CreateMATCHQuery as CMQ
from create_node_and_relationship import CreateNodeAndRelationship as CNAR
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

@app.route('/')
def main():
    return render_template("main.html")

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
    print(res)
    cn.close()
    return  jsonify(res)

@app.route('/post/create_node_and_relationship', methods=["GET"])
def get_node_and_relationship():
    node1 = request.args.get("node1")
    node2 = request.args.get("node2")
    relationship = request.args.get("relationship")
    return render_template("result.html", message="{}と{}は{}という関係を持ちます. ".format(node1, node2, relationship))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7878, debug=True)
