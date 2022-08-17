import sys,statistics
sys.path.append("/dic/neo4j")

from create_node_and_relationship import CreateNodeAndRelationship as CNAR

def c(node1, node2, type, relationship):
    cnar.create_Node(node_name=node1, type=type)
    cnar.create_Node(node_name=node2, type=type)
    cnar.create_relationship(node1, node2, relationship)

def s(node1, node2, score):
    cnar.create_Node(node_name=node1)
    cnar.create_Node(node_name=node2)
    cnar.create_score(node1, node2, score)

cnar = CNAR()
relationship = "have"
c("数と式", "数と集合", "数学I", relationship)
c("数と式", "式", "数学I",relationship)
c("二次関数", "二次関数とそのグラフ", "数学I", relationship)
c("二次関数", "二次関数の値の変化", "数学I", relationship)
c("データの分析", "データの散らばり", "数学I", relationship)
c("データの分析", "データの相関", "数学I", relationship)
s("シンジ", "数と集合", "70")
s("シンジ", "式", "40")
s("シンジ", "数と式", str(statistics.mean([70,40])))
s("シンジ", "二次関数とそのグラフ", "80")
s("シンジ", "二次関数の値の変化", "70")
s("シンジ", "二次関数", str(statistics.mean([80,70])))
s("シンジ", "データの散らばり", "30")
s("シンジ", "データの相関", "50")
s("シンジ", "データの分析", str(statistics.mean([30,50])))

cnar.close()