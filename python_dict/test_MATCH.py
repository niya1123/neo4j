import sys
sys.path.append("/dic/neo4j")
import json
from connection_neo4j import ConnectNeo4j as cn
from create_MATCH_query import CreateMATCHQuery as CMQ
from collections import defaultdict
from flask import Flask, jsonify, render_template, request, Response


# def return_json(result):
#     data = [record.data()["rel"] for record in result]
#     json_obj = "{"
#     for d in data:
#         json_obj += f"['parent':'{d[0]['name']}','children':'{d[2]['name']}','relationship':'{d[1]}'],"
#     json_obj += "}"
#     res = json.dumps(json_obj, ensure_ascii=False)
#     return res


def return_user_json(username,user_done_subject,user_subject_score):
    json_obj = defaultdict(list)
    json_obj['username'].append(username)
    for s in user_done_subject:
        json_obj['subject'].append(s)
    for ss in user_subject_score:   
        json_obj['score'].append(ss)
    json_obj = json.dumps(json_obj, ensure_ascii=False, default=str)
    res = Response(json_obj,content_type='application/json; charset=utf-8')
    res.status_code=200
    return res

def return_json(result):
    data = [record.data()['rel'] for record in result]
    json_obj = defaultdict(list)
    for d in data:
        json_obj['parent'].append(d[0]['name'])
        json_obj['children'].append(d[2]['name'])
        json_obj['relationship'].append(d[1])
    json_obj = json.dumps(json_obj, ensure_ascii=False, default=str)
    res = Response(json_obj,content_type='application/json; charset=utf-8')
    res.status_code=200
    return res

cn = cn()
session = cn.get_session()
username = "シンジ"
# result =session.run(CMQ._create_MATCH_query(node1_name="シンジ", node2_name="渚", relationship="親友"))
score_result = session.run(CMQ._create_MATCH_userscore_query(username))
user_done_subject = []
user_subject_score = []
for record in score_result:
    user_done_subject.append(record.data()['m.name'])
    user_subject_score.append(record.data()['rel.score'])
print(user_done_subject)
print(user_subject_score)
res = []
for subject in user_done_subject:
    subject_result = session.run(CMQ._create_MATCH_subject_query(subject))
    res.append(return_json(subject_result))
return_user_json(username, user_done_subject, user_subject_score)
cn.close()
