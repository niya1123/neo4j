from neo4j import GraphDatabase

class ConnectNeo4j:

    def __init__(self):
        """
        コンストラクタ. GraphDatabaseのdriveの生成を行う. 
        """
        scheme = "neo4j"
        host_name = "neo4j"
        port = 7687
        url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
        user = "neo4j"
        password = "test"
        self.driver = GraphDatabase.driver(url, auth=(user, password))
    
    def close(self):
        """
        driverを閉じる. 
        """
        self.driver.close()

    def get_session(self):
        """
        セッションのゲッター. 
        """
        return self.driver.session()