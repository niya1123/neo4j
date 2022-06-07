import sys
sys.path.append("/dic/neo4j")

from connection_neo4j import ConnectNeo4j as cn
from create_DELETE_query import CreateDELETEQuery as CDQ

cdq = CDQ(cn().driver)
cdq.run_DELETE(node_name="アスカ")