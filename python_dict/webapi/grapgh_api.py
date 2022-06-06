import sys
sys.path.append("/dic/neo4j")
import json
from connection_neo4j import ConnectNeo4j as cn
from create_MATCH_query import CreateMATCHQuery as cmq
from flask import Flask, jsonify, request
    
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cn = cn()
session = cn.get_session()
 
# @app.route('/')
# def hello_world():
#     return jsonify({'message': 'Hello world'})

@app.route('/', methods=["GET"])
def get_all_graph():
    result = session.run(cmq._create_MATCH_query())
    data = [record.data()['rel'] for record in result]
    json_obj = "{"
    for d in data:
        json_obj += f"['parent':'{d[0]['name']}','children':'{d[2]['name']}','relationship':'{d[1]}'],"
    json_obj += "}"
    res = json.dumps(json_obj, ensure_ascii=False)
    cn.close()
    return jsonify(res)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7878, debug=True)
