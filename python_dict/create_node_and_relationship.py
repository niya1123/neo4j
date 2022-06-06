from neo4j import GraphDatabase
from connection_neo4j import ConnectNeo4j as cn
from string import Template

class App:

    def __init__(self):
        """
        コンストラクタ. GraphDatabaseのdriveの生成を行う. 
        """
        self.cn = cn()
        self.driver = self.cn.driver

    def close(self):
        """
        driverを閉じる. 
        """
        self.cn.close()

    def create_Node(self, **kwargs):
        """
        ノードを作成する. 作れるノードは1つまで. 
        kwargsは{node_name: str, type: str, attr: str}が最大許容量．
        """
        with self.driver.session() as session:
            session.write_transaction(self._return_node, **kwargs)

    def create_relationship(self, node1_name, node2_name, relationship):
        """
        ノードとノードの関係を作成する. 
        """
        with self.driver.session() as session:
            session.write_transaction(self._return_relationship, node1_name, node2_name, relationship)

    @staticmethod
    def create_CREATE_query(**kwargs) -> str:
        """
        CREATEクエリを生成する. 
        """
        query = ""
        len_kwargs = len(kwargs)
        if len_kwargs == 1:
            query = Template("CREATE (n1:Node { name: '${node_name}' })").substitute(node_name=kwargs["node_name"])
        elif len_kwargs == 2:
            query = Template("CREATE (n1:${type} { name: '${node_name}' })").substitute(type=kwargs["type"], node_name=kwargs["node_name"])
        elif len_kwargs == 3:
            query = Template("CREATE (n1:${type} { ${attr}: '${attr_name}' })").substitute(type=kwargs["type"], attr=kwargs["attr"], attr_name=kwargs["node_name"])
        
        return query

    @staticmethod
    def _return_node(tx, **kwargs):
        """
        ノードを作成する. すでにあるノードは作成しない．
        """
        node_name = kwargs["node_name"]
        already_exist_query = (
                "MATCH (n) WHERE n.name = $node_name "
                "RETURN n"
            )
        result = tx.run(already_exist_query, node_name=node_name)
        if result.single() is None:
            query = App.create_CREATE_query(node_name=node_name)
            if len(kwargs) == 2:
                type = kwargs["type"]
                query = App.create_CREATE_query(node_name=node_name, type=type)
            elif len(kwargs) == 3:
                type = kwargs["type"]
                attr = kwargs["attr"]
                attr_name = kwargs["attr_name"]
                query = App.create_CREATE_query(attr_name=attr_name, type=type, attr=attr)
            tx.run(query)

    @staticmethod
    def _return_relationship(tx, node1_name, node2_name, relationship):
        """
        ノード間の関係性を生成. 
        """
        query = Template(
                "MATCH (n1),(n2) WHERE n1.name = '${node1_name}' AND n2.name = '${node2_name}' "
                "CREATE (n1)-[:${relationship}]->(n2) "
                "RETURN n1, n2"
            )
        tx.run(query.substitute(node1_name=node1_name, node2_name=node2_name, relationship=relationship))