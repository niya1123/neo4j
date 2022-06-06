import sys
sys.path.append("/dic/neo4j")
import json
from connection_neo4j import ConnectNeo4j as cn
# from create_MATCH_query import CreateMATCHQuery as cmq

cn = cn()
session = cn.get_session()
result = session.run("MATCH (n)-[rel]->(a) RETURN n, rel, a")
# print(json.dumps([record.data() for record in result], ensure_ascii=False))
data = [record.data()['rel'] for record in result]
json_obj = "{"
for d in data:
    json_obj += f"['parent':'{d[0]['name']}','children':'{d[2]['name']}','relationship':'{d[1]}'],"
json_obj += "}"
print(json_obj)
# print([record.data()['rel'] for record in result])
# print(type([record.data()['rel'] for record in result][0]))
cn.close()