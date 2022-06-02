import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from string import Template

class App:

    def __init__(self, uri, user, password):
        """
        コンストラクタ. GraphDatabaseのdriveの生成を行う. 
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        driverを閉じる. 
        """
        self.driver.close()

    def create_Node(self, node1_name, node2_name):
        """
        ノードを作成する. 
        """
        with self.driver.session() as session:
            session.write_transaction(self._return_node, node1_name, node2_name)

    def create_relationship(self, node1_name, node2_name, relationship):
        """
        ノードとノードの関係を作成する. 
        """
        with self.driver.session() as session:
            session.write_transaction(self._return_relationship, node1_name, node2_name, relationship)
          

    @staticmethod
    def _return_node(tx, node1_name, node2_name):
        """
        すでにあるノードは作成しない．
        """
        query_n1 = (
                "MATCH (n1:Node) WHERE n1.name = $node1_name "
                "RETURN n1"
            )
        query_n2 = (
            "MATCH (n2:Node) WHERE n2.name = $node2_name "
            "RETURN n2"
        )
        result_n1 = tx.run(query_n1, node1_name=node1_name)
        result_n2 = tx.run(query_n2, node2_name=node2_name)
        if result_n1.single() is None:
            query = (
                "CREATE (n1:Node { name: $node1_name }) "
            )
            tx.run(query, node1_name=node1_name)
        if result_n2.single() is None:
            query = (
                "CREATE (n2:Node { name: $node2_name }) "
            )
            tx.run(query, node2_name=node2_name)

    @staticmethod
    def _return_relationship(tx, node1_name, node2_name, relationship):
        """
        ノード間の関係性を生成. 
        """
        query = Template(
                "MATCH (n1:Node),(n2:Node) WHERE n1.name = '${node1_name}' AND n2.name = '${node2_name}' "
                "CREATE (n1)-[:${relationship}]->(n2) "
                "RETURN n1, n2"
            )
        tx.run(query.substitute(node1_name=node1_name, node2_name=node2_name, relationship=relationship))

if __name__ == "__main__":
    scheme = "neo4j"
    host_name = "neo4j"
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "test"
    app = App(url, user, password)
    while(True):
        n1 = input("1つめの名前を入れて: ")
        n2 = input("2つめの名前を入れて: ")
        app.create_Node(n1, n2)
        relationship = input("2ノードの関係性を入力してね: ")
        app.create_relationship(n1, n2, relationship)
        app.close()